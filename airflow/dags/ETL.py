from airflow.decorators import dag, task
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, mean, lead, lag, avg
from pyspark.sql.window import Window
import os

from utils.fetch_api import data_collection_api



DAG_ID = "ETL_TASKFLOW"

BRONZE_PATH = "/opt/airflow/data/Bronze/"
SILVER_PATH = "/opt/airflow/data/Silver/"

# ---------------- Spark ----------------
def get_spark():
    return SparkSession.builder \
        .appName("ETL_Taskflow") \
        .master("local[*]") \
        .config("spark.jars", "/opt/airflow/jars/postgresql-42.7.3.jar") \
        .getOrCreate()



# ---------------- Transform functions ----------------
def clean_nulls(df):
    for c in df.columns:
        nulls = df.filter(col(c).isNull()).count()
        if nulls > 0:
            mean_val = df.select(mean(c)).first()[0]
            if mean_val is not None:
                df = df.fillna({c: mean_val})
    return df

# ---------------- DAG ----------------
@dag(
    dag_id=DAG_ID,
    start_date=datetime(2026, 1, 21),
    schedule_interval=timedelta(minutes=15),
    catchup=False,
    tags=["spark", "etl"],
)
def etl_taskflow():

    @task
    def extract() -> str:
        spark = get_spark()

        pdf = data_collection_api(15, "1m", "BTCUSDT")
        sdf = spark.createDataFrame(pdf)

        sdf.write.mode("overwrite").parquet(BRONZE_PATH)
        return BRONZE_PATH

    @task
    def transform(bronze_path: str) -> str:
        spark = get_spark()
        df = spark.read.parquet(bronze_path)

        window = Window.orderBy("open_time")

        df = clean_nulls(df)
        df = df.drop("ignore").distinct()

        df = df.withColumn("close_t_plus_10", lead("close", 10).over(window))
        df = df.withColumn("prev_close", lag("close", 1).over(window))
        df = df.withColumn("return", (col("close") - col("prev_close")) / col("prev_close"))

        df = df.withColumn("MA_5", avg("close").over(window.rowsBetween(-5, -1)))
        df = df.withColumn("MA_10", avg("close").over(window.rowsBetween(-10, -1)))

        df = df.withColumn(
            "taker_ratio",
            col("taker_buy_base_volume") / col("volume")
        )

        df = clean_nulls(df)

        df.write.mode("overwrite").parquet(SILVER_PATH)
        return SILVER_PATH
    
    @task
    def save_silver_postgres(silver_path: str):
        spark = get_spark()
        jdbc_url = f"jdbc:postgresql://{os.environ.get('host')}:{os.environ.get('port')}/{os.environ.get('database')}"
        print(jdbc_url)
    
        connection_properties = {
            "user": os.environ.get('user'),
            "password": os.environ.get('password'),
            "driver": "org.postgresql.Driver"
        }

        print(connection_properties)

        df_load = spark.read.parquet(silver_path)

        df_load.write.jdbc(url=jdbc_url, table="silver_data_test", mode="append", properties=connection_properties)

    bronze = extract()
    silver = transform(bronze)
    save_silver_postgres(silver)

etl_taskflow()
