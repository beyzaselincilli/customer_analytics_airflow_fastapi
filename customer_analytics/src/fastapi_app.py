from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from dags.customer_analysis import CustomerAnalytics

app = FastAPI(title="Customer Analytics API", description="Müşteri analitiği işlemleri için API", version="1.0.0")

# CustomerAnalytics sınıfını başlat
analyzer = CustomerAnalytics()

# Veri yükleme modeli
class DataFile(BaseModel):
    filepath: str

# Tahmin isteği modeli
class PredictionRequest(BaseModel):
    months_ahead: int

@app.post("/load-data/")
async def load_data(data_file: DataFile):
    """Veri setini yükler ve temel temizleme işlemlerini gerçekleştirir."""
    try:
        data = analyzer.load_data(data_file.filepath)
        return {"message": "Veri başarıyla yüklendi", "shape": data.shape}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Veri yükleme hatası: {str(e)}")

@app.post("/preprocess-data/")
async def preprocess_data():
    """Veriyi ön işler."""
    try:
        data = analyzer.preprocess_data()
        return {"message": "Veri ön işleme tamamlandı", "columns": list(data.columns)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Veri ön işleme hatası: {str(e)}")

@app.post("/segment-customers/")
async def segment_customers(n_clusters: int = 4):
    """Müşteri segmentasyonu gerçekleştirir."""
    try:
        segments = analyzer.perform_customer_segmentation(n_clusters=n_clusters)
        return {"message": "Segmentasyon tamamlandı", "segments": segments.unique().tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Segmentasyon hatası: {str(e)}")

@app.post("/train-sales-model/")
async def train_sales_model():
    """Satış tahmin modelini eğitir."""
    try:
        metrics = analyzer.train_sales_prediction_model(analyzer.data)
        return {"message": "Model eğitimi tamamlandı", "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model eğitim hatası: {str(e)}")

@app.post("/predict-sales/")
async def predict_sales(request: PredictionRequest):
    """Gelecek dönem satış tahmini yapar."""
    try:
        predictions = analyzer.predict_future_sales(analyzer.data, months_ahead=request.months_ahead)
        return {"message": "Tahminler başarıyla oluşturuldu", "predictions": predictions.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tahmin hatası: {str(e)}")

@app.get("/")
async def root():
    """API'nin çalıştığını doğrulamak için basit bir endpoint."""
    return {"message": "Customer Analytics API çalışıyor!"}