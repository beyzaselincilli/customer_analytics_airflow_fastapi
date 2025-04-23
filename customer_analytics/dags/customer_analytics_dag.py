from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from customer_analysis import CustomerAnalytics
import pandas as pd

# CustomerAnalytics sınıfını başlat
analyzer = CustomerAnalytics()

# Varsayılan argümanlar
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG tanımı
with DAG(
    'customer_analytics_pipeline',
    default_args=default_args,
    description='Müşteri analitiği işlemleri için Airflow DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 4, 20),
    catchup=False,
) as dag:

    def load_data_task(**kwargs):
        """Veri yükleme işlemi."""
        data = analyzer.load_data('/opt/airflow/data/enterprise_customer_data.csv')
        # XCom ile veriyi paylaş
        kwargs['ti'].xcom_push(key='data', value=data.to_dict())

    def preprocess_data_task(**kwargs):
        """Veri ön işleme işlemi."""
        # XCom'dan veriyi al
        data_dict = kwargs['ti'].xcom_pull(key='data', task_ids='load_data')
        if data_dict is None:
            raise ValueError("Veri yüklenmeden ön işleme yapılamaz.")
        
        # Veriyi DataFrame'e dönüştür
        data = pd.DataFrame.from_dict(data_dict)
        analyzer.data = data

        # Örnek olarak recency, frequency, monetary sütunlarını oluşturun
        analyzer.data['recency'] = analyzer.data['last_order_days']  # Örnek bir hesaplama
        analyzer.data['frequency'] = analyzer.data['order_frequency']
        analyzer.data['monetary'] = analyzer.data['avg_order_value'] * analyzer.data['total_orders']

        analyzer.preprocess_data()

        # İşlenmiş veriyi XCom ile paylaş
        kwargs['ti'].xcom_push(key='processed_data', value=analyzer.data.to_dict())

    def segment_customers_task(**kwargs):
        """Müşteri segmentasyonu işlemi."""
        # XCom'dan işlenen veriyi al
        processed_data_dict = kwargs['ti'].xcom_pull(key='processed_data', task_ids='preprocess_data')
        if processed_data_dict is None:
            raise ValueError("İşlenmiş veri bulunamadı.")
        
        # Veriyi DataFrame'e dönüştür
        data = pd.DataFrame.from_dict(processed_data_dict)
        analyzer.data = data

        # Segmentasyon için gerekli sütunların mevcut olduğunu kontrol edin
        required_columns = ['recency', 'frequency', 'monetary']
        for col in required_columns:
            if col not in analyzer.data.columns:
                raise ValueError(f"Gerekli sütun eksik: {col}")

        analyzer.perform_customer_segmentation(n_clusters=4)

        # Segmentasyon sonrası veriyi XCom ile paylaş
        kwargs['ti'].xcom_push(key='segmented_data', value=analyzer.data.to_dict())

    def train_sales_model_task(**kwargs):
        """Satış tahmin modelini eğitme işlemi."""
        # XCom'dan segmentasyon sonrası veriyi al
        segmented_data_dict = kwargs['ti'].xcom_pull(key='segmented_data', task_ids='segment_customers')
        if segmented_data_dict is None:
            raise ValueError("Segmentasyon sonrası veri bulunamadı.")
        
        # Veriyi DataFrame'e dönüştür
        data = pd.DataFrame.from_dict(segmented_data_dict)
        analyzer.data = data

        # Satış tahmin modelini eğit
        analyzer.train_sales_prediction_model(analyzer.data)

    # Airflow görevleri
    load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_data_task,
        provide_context=True,
        dag=dag,
    )

    preprocess_data = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data_task,
        provide_context=True,
        dag=dag,
    )

    segment_customers = PythonOperator(
        task_id='segment_customers',
        python_callable=segment_customers_task,
        provide_context=True,
        dag=dag,
    )

    train_sales_model = PythonOperator(
        task_id='train_sales_model',
        python_callable=train_sales_model_task,
        provide_context=True,
        dag=dag,
    )

    # Görev sıralaması
    load_data >> preprocess_data >> segment_customers >> train_sales_model