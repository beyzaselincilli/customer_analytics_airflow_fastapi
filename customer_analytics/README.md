# Kurumsal Müşteri Analitik Platformu

Bu proje, kurumsal müşteri verilerini analiz eden, müşteri segmentasyonu yapan ve gelecekteki satışları tahmin eden kapsamlı bir veri bilimi uygulamasıdır. Backend, **FastAPI** framework'ü ile geliştirilmiş olup, **Airflow** ile veri işleme süreçleri otomatikleştirilmiştir.

---

## Özellikler

- 🔍 **Müşteri Segmentasyonu**: RFM analizi ve K-means clustering
- 📈 **Satış Tahmin Modeli**: XGBoost regresyon modeli
- 📊 **Otomatik Veri İşleme**: Airflow DAG'ları ile veri işleme otomasyonu
- 📱 **Swagger Dokümantasyonu**: FastAPI ile otomatik API dokümantasyonu
- 📝 **Otomatik Raporlama**: Model sonuçlarının raporlanması
- 📊 **MLflow ile Model Takibi**: Model performans metriklerinin izlenmesi

---

## Kurulum

### 1. Gerekli Bağımlılıkları Yükleyin
Proje bağımlılıklarını yüklemek için:
```bash
pip install -r [requirements.txt](http://_vscodecontentref_/0)

2. Docker ile Servisleri Başlatın
Tüm servisleri Docker Compose ile başlatmak için:
docker-compose up --build

3. FastAPI Uygulamasını Çalıştırın
FastAPI uygulamasını manuel olarak çalıştırmak isterseniz:
cd src
uvicorn fastapi_app:app --reload

4. Airflow Web Arayüzüne Erişim
Airflow web arayüzüne erişmek için tarayıcınızda şu adrese gidin:
http://localhost:8080

5. FastAPI Swagger Arayüzüne Erişim
FastAPI'nin otomatik oluşturulan Swagger dokümantasyonuna erişmek için:
http://localhost:8000/docs


Veri Formatı
Uygulamanın beklediği CSV dosyası formatı:

customer_id: Müşteri ID
recency: Son alışverişten bu yana geçen gün sayısı
frequency: Toplam alışveriş sayısı
monetary: Toplam harcama tutarı
sales: Aylık ortalama satış tutarı
[diğer özellikler]: Demografik ve davranışsal özellikler

Proje Yapısı
customer_analytics/
├── data/               # Veri dosyaları
├── dags/               # Airflow DAG'ları
│   ├── customer_analytics_dag.py
│   └── __init__.py
├── notebooks/          # Jupyter notebooks
├── src/                # Backend kaynak kodları
│   ├── fastapi_app.py  # FastAPI uygulaması
│   ├── customer_analysis.py
│   └── models/         # Model dosyaları
├── models/             # Eğitilmiş modeller
├── reports/            # Otomatik oluşturulan raporlar
├── Dockerfile          # Airflow için Dockerfile
├── [Dockerfile.fastapi](http://_vscodecontentref_/1)  # FastAPI için Dockerfile
├── [docker-compose.yaml](http://_vscodecontentref_/2) # Docker Compose yapılandırması
└── [requirements.txt](http://_vscodecontentref_/3)    # Bağımlılıklar

Teknik Detaylar
Müşteri Segmentasyonu
RFM (Recency, Frequency, Monetary) analizi
K-means clustering algoritması
Optimal küme sayısı belirleme
Satış Tahmin Modeli
XGBoost regresyon modeli
Özellik önem analizi
Cross-validation
Model performans metrikleri
Backend (FastAPI)
RESTful API tasarımı
Swagger dokümantasyonu
JSON tabanlı veri işleme
Hata yönetimi ve loglama

Veri İşleme (Airflow)
Airflow DAG'ları ile otomatik veri işleme
XCom ile veri paylaşımı
Günlük veya saatlik veri işleme görevleri
Katkıda Bulunma
1.Bu depoyu fork edin.
2.Yeni bir branch oluşturun:
git checkout -b feature/yeni-ozellik

3. Değişikliklerinizi commit edin
git commit -m "Yeni özellik eklendi"

4.Branch'inizi push edin
git push origin feature/yeni-ozellik

5.Pull Request oluşturun.

---

### Güncellemeler
- **FastAPI ve Airflow**: Projenin hem FastAPI hem de Airflow bileşenlerini kapsadığı belirtilmiştir.
- **Docker Kullanımı**: Docker Compose ile servislerin nasıl başlatılacağı açıklanmıştır.
- **Swagger ve Airflow Arayüzleri**: İlgili URL'ler eklenmiştir.
- **Proje Yapısı**: Dosya ve klasör yapısı detaylandırılmıştır.

Eğer başka bir ekleme veya düzenleme gerekiyorsa, lütfen belirtin! 😊