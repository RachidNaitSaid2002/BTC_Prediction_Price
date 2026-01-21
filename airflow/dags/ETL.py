from airflow.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, mean, lead, lag, avg
from pyspark.sql.window import Window
import requests
import pandas as pd

DAG_ID = "ETL"

def get_spark():
    spark = SparkSession.builder.appName("App").getOrCreate()
    return spark

def data_collection_api(LIMIT, INTERVAL, SYMBOL):
    response = requests.get(
        url='https://api.binance.com/api/v3/klines',
        params={
            "symbol": SYMBOL,
            "interval": INTERVAL,
            "limit": LIMIT
        }
    )
    
    if response.status_code != 200:
        print(f"Erreur {response.status_code}")
        return None
    
    data = response.json()
    
    columns = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ]
    
    # Créer un DataFrame pandas
    df = pd.DataFrame(data, columns=columns)
    
    numeric_cols = ["open", "high", "low", "close", "volume", "quote_asset_volume", "taker_buy_base_volume", "taker_buy_quote_volume"]
    df[numeric_cols] = df[numeric_cols].astype(float)
    
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
    
    return df

def load_data():
    output_path = "/media/rachid/d70e3dc6-74e7-4c87-96bc-e4c3689c979a/lmobrmij/Projects/BTC_Prediction_Price/ml/Data/Normal/btc_minute_data.parquet"
    spark = get_spark()
    df = spark.read.parquet(output_path)
    return df

def Save_Bronze_Local(Data_i):
    Data_i.write.mode('overwrite').format("parquet").save("/media/rachid/d70e3dc6-74e7-4c87-96bc-e4c3689c979a/lmobrmij/Projects/BTC_Prediction_Price/ml/testdata/Bronze/")

def CheckNull(Data_B):
    num_rows = Data_B.count()       
    Columns_list = Data_B.columns

    for c in Columns_list:
        num_null = Data_B.filter(col(c).isNull()).count()
        if num_null > 0:
            null_percent = (num_null / num_rows) * 100
            print(f"Column {c} has {num_null} null values ({null_percent:.2f}%)")
            
            if null_percent < 5:
                Data_B = Data_B.na.drop(subset=[c])
            else:
                try:
                    mean_value = Data_B.select(mean(c)).collect()[0][0]
                    Data_B = Data_B.fillna({c: mean_value})
                except:
                    mode_value = Data_B.groupBy(c).count().orderBy(col("count").desc()).first()[0]
                    Data_B = Data_B.fillna({c: mode_value})
        else:
            print(f"{c} : you dont have any null values")
    return Data_B

def CheckDuplicated(Data_B):
    num_rows = Data_B.count()
    num_rows_no_duplicate = Data_B.distinct().count()
    num_duplicate_values = num_rows - num_rows_no_duplicate
    if num_duplicate_values == 0:
        print("you don't have any duplicated values !!")
    else:
        Data_B = Data_B.distinct()
        return Data_B
    return Data_B

def Ignore_Remover(Data_B):
    Data_B = Data_B.drop(col("ignore"))
    return Data_B

def Create_Column_close_t_plus_10(Data_B):
    window = Window.orderBy("open_time")
    Data_B = Data_B.withColumn("close_t_plus_10", lead("close", 10).over(window))
    return Data_B

def Entry_Creator(Data_B):

    windowSpec = Window.orderBy("open_time")

    Data_B = Data_B.withColumn(
        "prev_close",
        lag("close", 1).over(windowSpec)
    )

    Data_B = Data_B.withColumn(
        "return",
        (col("close") - col("prev_close")) / col("prev_close")
    )

    return Data_B

def MA5_Creator(Data_B):
    window = Window.orderBy("open_time")
    Window_5 = window.rowsBetween(-4, 0)
    Data_B = Data_B.withColumn("MA_5", avg(col("close")).over(Window_5))
    return Data_B

def MA10_Creator(Data_B):
    window = Window.orderBy("open_time")
    Window_10 = window.rowsBetween(-9, 0)
    Data_B = Data_B.withColumn("MA_10", avg(col("close")).over(Window_10))
    return Data_B

def takerratio_creator(Data_B):
    Data_B = Data_B.withColumn("taker_ratio", col("taker_buy_base_volume") / col("volume"))
    return Data_B

def Save_Silver_Local(Data_B):
    Data_B.write.mode('overwrite').format("parquet").save("/media/rachid/d70e3dc6-74e7-4c87-96bc-e4c3689c979a/lmobrmij/Projects/BTC_Prediction_Price/ml/testdata/Silver/")


# Extract :
def Extract_Data():
    df = data_collection_api(15, "1m", "BTCUSDT")
    df = load_data()
    Save_Bronze_Local(df)

#Transform :
def Transform_Data():
    df = load_data()
    df = CheckNull(df)
    df = CheckDuplicated(df)
    df = Ignore_Remover(df)
    df = Create_Column_close_t_plus_10(df)
    df = CheckNull(df)
    df = Entry_Creator(df)
    df = CheckNull(df)
    df = MA5_Creator(df)
    df = CheckNull(df)
    df = MA10_Creator(df)
    df = CheckNull(df)
    df = takerratio_creator(df)
    df = CheckNull(df)
    Save_Silver_Local(df)


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 1, 21),
}

dag = DAG(DAG_ID, default_args=default_args, schedule_interval=timedelta(minutes=15), catchup=False)

task_Extract = PythonOperator(
    task_id='Extract_data',
    python_callable=Extract_Data,
    dag=dag,
)

task_Transform = PythonOperator(
    task_id='transform_data',
    python_callable=Transform_Data,
    dag=dag,
)

task_Extract >> task_Transform