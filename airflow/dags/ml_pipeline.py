from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta
from pyspark.sql import Window, SparkSession
from pyspark.sql.functions import col, row_number, max as spark_max, min as spark_min
import os
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.regression import RandomForestRegressor, RandomForestRegressionModel
from pyspark.ml.evaluation import RegressionEvaluator


# Configuration
DAG_ID = "ml_pipeline"
MODEL_OUTPUT_PATH = "/opt/airflow/data/models"
FEATURE_COLS = ["MA_5", "high", "low", "open", "close", "MA_10", "prev_close", "return"]
TARGET_COL = "close_t_plus_10"

# Paramètres du modèle
RF_NUM_TREES = 100
RF_MAX_DEPTH = 10
RF_MIN_INSTANCES = 5
TRAIN_RATIO = 0.8


def get_spark():
    return SparkSession.builder \
        .appName("BitcoinML") \
        .master("local[*]") \
        .config("spark.jars", "/opt/airflow/jars/postgresql-42.7.3.jar") \
        .getOrCreate()


def load_data(**context):
    """Charge les données récentes depuis PostgreSQL"""
    spark = get_spark()
    os.makedirs("/opt/airflow/data/temp", exist_ok=True)
    
    jdbc_url = f"jdbc:postgresql://{os.environ.get('host')}:{os.environ.get('port')}/{os.environ.get('database')}"
    connection_properties = {
        "user": os.environ.get('user'),
        "password": os.environ.get('password'),
        "driver": "org.postgresql.Driver"
    }
    
    # Charger les 10 000 dernières lignes
    query = """
        (SELECT * FROM silver_data_test 
         ORDER BY open_time ASC) as recent_data
    """
    
    print("Chargement des données depuis PostgreSQL...")
    
    df = spark.read.jdbc(
        url=jdbc_url,
        table=query,
        properties=connection_properties
    )
    
    # Re-trier par ordre chronologique
    df = df.orderBy("open_time")
    
    row_count = df.count()
    if row_count == 0:
        raise ValueError("Aucune donnée dans silver_data_test")
     
    if row_count < 500:  # Vérifier qu'il y a assez de données
        print(f"ATTENTION: Seulement {row_count} lignes - risque de problèmes!")
    
    
    print(f"✓ {row_count} lignes chargées depuis PostgreSQL")
    
    temp_path = "/opt/airflow/data/temp/raw_data.parquet"
    df.write.mode("overwrite").parquet(temp_path)
    context['ti'].xcom_push(key='raw_data_path', value=temp_path)


def prepare_ml_data(df, feature_names, target_col, train_ratio):
    """Prépare les données pour le ML"""
    print("=" * 50)
    print("Préparation des données")
    print("=" * 50)
    
    # Vérification des colonnes
    missing_cols = set(feature_names + [target_col]) - set(df.columns)
    if missing_cols:
        raise ValueError(f"✗ Colonnes manquantes: {missing_cols}")
    
    print("✓ Toutes les colonnes présentes")
    
    # Vérifier les nulls
    for col_name in feature_names + [target_col]:
        null_count = df.filter(col(col_name).isNull()).count()
        if null_count > 0:
            print(f"  ⚠ {col_name}: {null_count} valeurs nulles")
    
    # Vectorisation
    assembler = VectorAssembler(
        inputCols=feature_names,
        outputCol="features_raw",
        handleInvalid="skip"
    )
    df = assembler.transform(df)
    
    # Index temporel
    window = Window.orderBy("open_time")
    df = df.withColumn("time_index", row_number().over(window))
    
    # Split temporel
    total_rows = df.count()
    split_point = int(total_rows * train_ratio)
    
    df_train_raw = df.filter(col("time_index") <= split_point)
    df_test_raw = df.filter(col("time_index") > split_point)
    
    print(f"\nSplit: {int(train_ratio*100)}% train / {int((1-train_ratio)*100)}% test")
    print(f"  Train: {df_train_raw.count()} lignes")
    print(f"  Test:  {df_test_raw.count()} lignes")
    
    # Normalisation (fit sur train uniquement)
    scaler = StandardScaler(
        inputCol="features_raw",
        outputCol="features",
        withStd=True,
        withMean=True
    )
    
    scaler_model = scaler.fit(df_train_raw)
    df_train = scaler_model.transform(df_train_raw)
    df_test = scaler_model.transform(df_test_raw)
    
    # Vérification anti-fuite temporelle
    train_max_time = df_train.agg(spark_max("open_time")).collect()[0][0]
    test_min_time = df_test.agg(spark_min("open_time")).collect()[0][0]
    
    if train_max_time >= test_min_time:
        raise ValueError("✗ FUITE TEMPORELLE DÉTECTÉE!")
     
    print(f"\n  DEBUG: train_max_time = {train_max_time}")
    print(f"  DEBUG: test_min_time = {test_min_time}")
    
    print(f"✓ Pas de fuite temporelle")
    print("=" * 50)
    
    return df_train, df_test, scaler_model


def prepare_data(**context):
    """Prépare les données pour le ML"""
    raw_path = context['ti'].xcom_pull(key='raw_data_path', task_ids='load_data')
    spark = get_spark()
    df = spark.read.parquet(raw_path)
    
    os.makedirs(MODEL_OUTPUT_PATH, exist_ok=True)
    
    df_train, df_test, scaler_model = prepare_ml_data(
        df, FEATURE_COLS, TARGET_COL, TRAIN_RATIO
    )
    
    # Sauvegarder
    train_path = "/opt/airflow/data/temp/train.parquet"
    test_path = "/opt/airflow/data/temp/test.parquet"
    scaler_path = f"{MODEL_OUTPUT_PATH}/scaler"
    
    df_train.write.mode("overwrite").parquet(train_path)
    df_test.write.mode("overwrite").parquet(test_path)
    scaler_model.write().overwrite().save(scaler_path)
    
    context['ti'].xcom_push(key='train_path', value=train_path)
    context['ti'].xcom_push(key='test_path', value=test_path)


def train_random_forest(**context):
    """Entraîne le modèle Random Forest"""
    print("\n" + "=" * 50)
    print("TRAINING - RANDOM FOREST")
    print("=" * 50)
    
    train_path = context['ti'].xcom_pull(key='train_path', task_ids='prepare_data')
    spark = get_spark()
    df_train = spark.read.parquet(train_path)
    
    print(f"\nConfiguration:")
    print(f"  Arbres: {RF_NUM_TREES}")
    print(f"  Profondeur max: {RF_MAX_DEPTH}")
    print(f"  Min instances/noeud: {RF_MIN_INSTANCES}")
    
    rf = RandomForestRegressor(
        featuresCol="features",
        labelCol=TARGET_COL,
        numTrees=RF_NUM_TREES,
        maxDepth=RF_MAX_DEPTH,
        minInstancesPerNode=RF_MIN_INSTANCES,
        seed=42
    )
    
    print("\nEntraînement en cours...")
    model = rf.fit(df_train)
    
    # Sauvegarder
    model_path = f"{MODEL_OUTPUT_PATH}/random_forest"
    model.write().overwrite().save(model_path)
    
    print(f"✓ Modèle sauvegardé: {model_path}")
    print("=" * 50)


def evaluate_random_forest(**context):
    """Évalue le modèle Random Forest"""
    print("\n" + "=" * 50)
    print("ÉVALUATION - RANDOM FOREST")
    print("=" * 50)
    
    test_path = context['ti'].xcom_pull(key='test_path', task_ids='prepare_data')
    spark = get_spark()
    df_test = spark.read.parquet(test_path)
    
    # Charger le modèle
    model = RandomForestRegressionModel.load(f"{MODEL_OUTPUT_PATH}/random_forest")
    
    # Prédictions
    predictions = model.transform(df_test)
    
    # Métriques
    evaluator_rmse = RegressionEvaluator(
        labelCol=TARGET_COL, 
        predictionCol="prediction", 
        metricName="rmse"
    )
    evaluator_mae = RegressionEvaluator(
        labelCol=TARGET_COL, 
        predictionCol="prediction", 
        metricName="mae"
    )
    evaluator_r2 = RegressionEvaluator(
        labelCol=TARGET_COL, 
        predictionCol="prediction", 
        metricName="r2"
    )
    
    rmse = evaluator_rmse.evaluate(predictions)
    mae = evaluator_mae.evaluate(predictions)
    r2 = evaluator_r2.evaluate(predictions)
    
    print(f"\nRésultats:")
    print(f"  RMSE: ${rmse:.2f}")
    print(f"  MAE:  ${mae:.2f}")
    print(f"  R²:   {r2:.4f}")
    
    # Exemples de prédictions
    print("\nExemples de prédictions:")
    predictions.select(TARGET_COL, "prediction").show(5, truncate=False)
    
    print("=" * 50)


# ========== Configuration DAG ==========
default_args = {
   'owner': 'airflow',
   'depends_on_past': False,
   'start_date': datetime(2026, 1, 21),
   'email_on_failure': False,
   'retries': 1,
   'retry_delay': timedelta(minutes=5),
}

dag = DAG(
   DAG_ID,
   default_args=default_args,
   description='Pipeline ML Bitcoin',
   schedule_interval=timedelta(minutes=15),
   catchup=False,
   tags=['ml', 'bitcoin']
)


# ========== Définition des tâches ==========

# Attendre que l'ETL soit terminé
wait_for_etl = ExternalTaskSensor(
    task_id='wait_for_etl',
    external_dag_id='ETL_TASKFLOW',
    external_task_id='save_silver_postgres',
    mode='reschedule',
    poke_interval=30,
    timeout=900,
    allowed_states=['success'],
    dag=dag
)

task_load = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    provide_context=True,
    dag=dag
)

task_prepare = PythonOperator(
    task_id='prepare_data',
    python_callable=prepare_data,
    provide_context=True,
    dag=dag
)

task_train = PythonOperator(
    task_id='train_random_forest',
    python_callable=train_random_forest,
    provide_context=True,
    dag=dag
)

task_evaluate = PythonOperator(
    task_id='evaluate_random_forest',
    python_callable=evaluate_random_forest,
    provide_context=True,
    dag=dag
)


# ========== Pipeline ==========
wait_for_etl >> task_load >> task_prepare >> task_train >> task_evaluate

# task_load >> task_prepare >> task_train >> task_evaluate