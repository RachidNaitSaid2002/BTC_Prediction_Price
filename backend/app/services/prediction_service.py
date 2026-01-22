from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from ..core.config import settings
from ..schemas.PredictionRequest_schema import PredictRequest

class PredictionService:
    def __init__(self, model_path: str = settings.MODEL_PATH):
        self.spark = SparkSession.builder \
            .appName("CryptoPrediction") \
            .master("local[*]") \
            .config("spark.driver.memory", "2g") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("ERROR")
        self.model = PipelineModel.load(model_path)
    
    def predict(self, request: PredictRequest) -> float:
        data = [{
            "MA_5": float(request.MA_5),
            "high": float(request.high),
            "low": float(request.low),
            "open": float(request.open),
            "close": float(request.close),
            "MA_10": float(request.MA_10),
            "prev_close": float(request.prev_close),
            "return": float(request.return_val)
        }]
        
        df = self.spark.createDataFrame(data)
        prediction = self.model.transform(df)
        result = prediction.select("prediction").first()[0]
        
        return float(result)
    
    def close(self):
        self.spark.stop()

prediction_service = None

def get_prediction_service() -> PredictionService:
    global prediction_service
    if prediction_service is None:
        prediction_service = PredictionService()
    return prediction_service