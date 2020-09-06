import os

from google.cloud import storage


def download_file(file_name):
    storage_client = storage.Client()

    bucket = storage_client.bucket(os.getenv('BUCKET_NAME'))
    blob = bucket.blob(file_name)
    name = f'models/{file_name.split("/")[-1]}'
    blob.download_to_filename(name)
    print(f'File downloaded {name}')
    return name


def get_blobs():
    print(os.getenv('BUCKET_NAME'))
    storage_client = storage.Client()

    blobs = storage_client.list_blobs(os.getenv('BUCKET_NAME'))
    b = list()
    for blob in blobs:
        b.append(blob.name)

    return b
