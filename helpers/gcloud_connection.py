import os

from google.cloud import storage


class gcloud_connection:
    def download_file(self, file_name):
        storage_client = storage.Client()

        bucket = storage_client.bucket(os.getenv('BUCKET_NAME'))
        blob = bucket.blob(file_name)
        name = f'models/{file_name.split("/")[-1]}'
        blob.download_to_filename(name)
        print(f'File downloaded {name}')
        return name
