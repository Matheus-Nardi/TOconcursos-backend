import os
from io import BytesIO
from urllib.parse import urlparse
from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error

class UploadService: 
    def __init__(self):
        """
        Inicializa o cliente MinIO usando as variáveis de ambiente carregadas do .env
        """
        load_dotenv()
        self.endpoint = os.getenv("MINIO_ENDPOINT")
        self.access_key = os.getenv("MINIO_ACCESS_KEY")
        self.secret_key = os.getenv("MINIO_SECRET_KEY")
        self.bucket_name = os.getenv("MINIO_BUCKET", "uploads")
        self.public_url = os.getenv("MINIO_PUBLIC_URL", f"http://{self.endpoint}")
       
        self.minio_client = Minio(
            endpoint=self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=False 
        )

        if not self.minio_client.bucket_exists(self.bucket_name):
            self.minio_client.make_bucket(self.bucket_name)


    def upload_file(self, file_path: str, file_data: bytes, content_type: str) -> str:
        """
        Faz upload de um arquivo para o bucket do MinIO.

        :param file_path: Caminho/nome do arquivo dentro do bucket.
        :param file_data: Dados binários do arquivo.
        :param content_type: Tipo MIME do arquivo.
        :return: URL do arquivo enviado.
        """
        try:
            # Envia o arquivo
            self.minio_client.put_object(
                bucket_name=self.bucket_name,
                object_name=file_path,
                data=BytesIO(file_data),
                length=len(file_data),
                content_type=content_type
            )

            # Monta a URL de acesso
            file_url = f"{self.public_url}/{self.bucket_name}/{file_path}"
            return file_url

        except S3Error as e:
            raise Exception(f"Erro ao fazer upload no MinIO: {e}")
        

    def delete_file(self, file_path: str):
        self.minio_client.remove_object(self.bucket_name, file_path)

    def get_file_path_from_url(self, file_url: str) -> str:
        parsed = urlparse(file_url)
        path_parts = parsed.path.split('/', 2)
        return path_parts[2] if len(path_parts) > 2 else ''