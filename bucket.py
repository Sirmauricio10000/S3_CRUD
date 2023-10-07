import boto3
import os
from keys import access_key, secret_access_key

s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)
download_directory = './download' 
bucket_name = 'mauriciobucket1907'  


def upload_to_bucket(ruta, nombre):
    try:
        s3_client.upload_file(ruta, bucket_name, nombre)
        print(f"Archivo '{nombre}' cargado en el bucket '{bucket_name}'.")
        return True
    except Exception as e:
        print(f"Error al cargar el archivo en el bucket: {str(e)}")
        return str(e)

def delete_from_bucket(nombre):
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=nombre)
        print(f"Archivo '{nombre}' eliminado del bucket '{bucket_name}'.")
        return True
    except Exception as e:
        print(f"Error al eliminar el archivo del bucket: {str(e)}")
        return str(e)
    
def download_from_bucket(nombre):
    try:
        ruta_destino = os.path.join(download_directory, nombre)
        s3_client.download_file(bucket_name, nombre, ruta_destino)
        
        print(f"Archivo '{nombre}' descargado del bucket '{bucket_name}' y guardado en '{ruta_destino}'.")
        return ruta_destino  # Devuelve la ruta donde se guardó el archivo descargado
    except Exception as e:
        print(f"Error al descargar el archivo del bucket: {str(e)}")
        return str(e)

