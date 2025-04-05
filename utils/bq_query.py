from google.cloud import bigquery
import os


def get_bq_client(key_path="../imdb-dataset-privateKey.json"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
    try:
        client = bigquery.Client()
        print("✅ BigQuery клиент успешно создан")
        return client
    except Exception as e:
        print("❌ Ошибка при создании клиента BigQuery:", e)
        raise


def run_query(client, query: str):
    return client.query(query).to_dataframe()
