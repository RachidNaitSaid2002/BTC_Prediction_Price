

def load_silver_data(silver_path):
    """
    Charge les données depuis la zone Silver (format Parquet)
    """
    from pyspark.sql import SparkSession

    
    if not parquet_files:
        raise FileNotFoundError("Aucun fichiertrouvé")

    df_silver = spark.read.parquet("../../Data/Silver")

    return df
