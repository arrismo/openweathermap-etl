from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
import json
from airflow.operators.python import PythonOperator
import pandas as pd

def kelvin_to_fahrenheit(temp_in_kelvin):
    temp_in_fahrenheit = (temp_in_kelvin - 273.15) * (9/5) + 32
    return temp_in_fahrenheit


def transform_load_data(task_instance):
    data = task_instance.xcom_pull(task_ids="extract_weather_data")
    
    # Get city information
    city = data["city"]["name"]
    sunrise_time = datetime.utcfromtimestamp(data['city']['sunrise'] + data['city']['timezone']).strftime('%Y-%m-%d %H:%M:%S')
    sunset_time = datetime.utcfromtimestamp(data['city']['sunset'] + data['city']['timezone']).strftime('%Y-%m-%d %H:%M:%S')
    
    transform_data = []
    for item in data['list']:
        transformed_record = {
            'city':city,
            'sunrise': sunrise_time,
            'sunset': sunset_time,
            'time_of_record': item['dt_txt'],
            'temp_farenheit': kelvin_to_fahrenheit(item["main"]["temp"]),
            'feels_like_farenheit': kelvin_to_fahrenheit(item["main"]["feels_like"]),
            'min_temp_farenheit' :kelvin_to_fahrenheit(item["main"]["temp_min"]),
            'max_temp_farenheit' : kelvin_to_fahrenheit(item["main"]["temp_max"]),
            'weather_description' : item['weather'][0]['description'],
            'pressure': item["main"]["pressure"],
            'humidity': item["main"]["humidity"],
            'wind_speed': item["wind"]["speed"]     
        }
        transform_data.append(transformed_record)
       
    df_data = pd.DataFrame(transform_data)

    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    dt_string = 'current_weather_data_newyork_' + dt_string
    df_data.to_csv(f"s3://weatherapiairflowbuckettutorial/{dt_string}.csv",index=False)




default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024,11,23),
    'email': [],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}



with DAG('weather_dag',
         default_args=default_args,
         schedule_interval = '@daily',
         catchup=False) as dag:

        is_weather_api_ready = HttpSensor(
            task_id='is_weather_api_ready',
            http_conn_id='weathermap_api',
            endpoint="/data/2.5/forecast?q=New York&APPID={{ conn.get('weathermap_api').extra_dejson['api_key'] }}",
        )
        
        extract_weather_data = SimpleHttpOperator(
            task_id = 'extract_weather_data',
            http_conn_id = 'weathermap_api',
            endpoint="/data/2.5/forecast?q=New York&APPID={{ conn.get('weathermap_api').extra_dejson['api_key'] }}",
            method = 'GET',
            response_filter= lambda r: json.loads(r.text),
            log_response=True
        )
        
        transform_load_weather_data = PythonOperator(
            task_id= 'transform_load_weather_data',
            python_callable=transform_load_data
        )
        
        is_weather_api_ready >> extract_weather_data >> transform_load_weather_data
    