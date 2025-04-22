from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from customer_analysis import CustomerAnalytics

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

    def load_data_task():
        """Veri yükleme işlemi."""
        analyzer.load_data('../data/enterprise_customer_data.csv')

    def preprocess_data_task():
        """Veri ön işleme işlemi."""
        analyzer.preprocess_data()

    def segment_customers_task():
        """Müşteri segmentasyonu işlemi."""
        analyzer.perform_customer_segmentation(n_clusters=4)

    def train_sales_model_task():
        """Satış tahmin modelini eğitme işlemi."""
        analyzer.train_sales_prediction_model(analyzer.data)

    # Airflow görevleri
    load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_data_task,
    )

    preprocess_data = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data_task,
    )

    segment_customers = PythonOperator(
        task_id='segment_customers',
        python_callable=segment_customers_task,
    )

    train_sales_model = PythonOperator(
        task_id='train_sales_model',
        python_callable=train_sales_model_task,
    )

    # Görev sıralaması
    load_data >> preprocess_data >> segment_customers >> train_sales_model