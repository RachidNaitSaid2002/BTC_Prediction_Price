from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType
from ..core.config import settings
from ..schemas.prediction import PredictRequest

class PredictionService:
    def __init__(self, model_path: str = settings.MODEL_PATH):
        self.spark = SparkSession.builder \
            .appName("CryptoPrediction") \
            .master("local[*]") \
            .config("spark.driver.memory", "2g") \
            .getOrCreate()
        
        self.model = PipelineModel.load(model_path)
        
        # Schéma Spark
        self.schema = StructType([
            StructField("MA_5", DoubleType(), False),
            StructField("high", DoubleType(), False),
            StructField("low", DoubleType(), False),
            StructField("open", DoubleType(), False),
            StructField("close", DoubleType(), False),
            StructField("MA_10", DoubleType(), False),
            StructField("prev_close", DoubleType(), False),
            StructField("return", DoubleType(), False)
        ])
    
    def predict(self, request: PredictRequest) -> float:
        # Convertir en dict pour Spark
        data = {
            "MA_5": request.MA_5,
            "high": request.high,
            "low": request.low,
            "open": request.open,
            "close": request.close,
            "MA_10": request.MA_10,
            "prev_close": request.prev_close,
            "return": request.return_val
        }
        
        # Créer DataFrame et prédire
        df = self.spark.createDataFrame([data], schema=self.schema)
        prediction = self.model.transform(df)
        result = prediction.select("prediction").first()[0]
        
        return float(result)
    
    def close(self):
        self.spark.stop()

# Singleton
prediction_service = None

def get_prediction_service() -> PredictionService:
    global prediction_service
    if prediction_service is None:
        prediction_service = PredictionService()
    return prediction_service