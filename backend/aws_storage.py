import boto3
import os
from datetime import datetime
from typing import List, Dict, Optional
from botocore.exceptions import ClientError, NoCredentialsError
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AWSStorageManager:
    def __init__(self):
        self.s3_client = None
        self.bucket_name = os.getenv('AWS_S3_BUCKET', 'my-file-storage-bucket')
        self.region_name = os.getenv('AWS_REGION', 'us-east-1')
        self._initialize_s3_client()
    
    def _initialize_s3_client(self):
        """Inicializa o cliente S3 com credenciais do ambiente"""
        try:
            # Tenta usar credenciais do ambiente (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
            self.s3_client = boto3.client(
                's3',
                region_name=self.region_name
            )
            # Testa a conexão
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logger.info(f"Conectado ao bucket S3: {self.bucket_name}")
        except NoCredentialsError:
            logger.error("Credenciais AWS não encontradas. Configure AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY")
            raise
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                logger.error(f"Bucket {self.bucket_name} não encontrado")
                raise
            elif error_code == '403':
                logger.error(f"Acesso negado ao bucket {self.bucket_name}")
                raise
            else:
                logger.error(f"Erro ao conectar com S3: {e}")
                raise
    
    def get_user_folder(self, username: str) -> str:
        """Retorna o caminho da pasta do usuário"""
        return f"users/{username}/"
    
    def list_files(self, username: str) -> List[Dict]:
        """Lista todos os arquivos do usuário"""
        try:
            user_folder = self.get_user_folder(username)
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=user_folder
            )
            
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    # Remove o prefixo da pasta do usuário
                    file_key = obj['Key']
                    if file_key != user_folder:  # Não incluir a pasta em si
                        file_name = file_key.replace(user_folder, '')
                        files.append({
                            'key': file_key,
                            'name': file_name,
                            'size': obj['Size'],
                            'last_modified': obj['LastModified'].isoformat(),
                            'etag': obj['ETag'].strip('"')
                        })
            
            return files
        except ClientError as e:
            logger.error(f"Erro ao listar arquivos: {e}")
            raise
    
    def upload_file(self, username: str, file_content: bytes, file_name: str, content_type: str = None) -> Dict:
        """Faz upload de um arquivo para o S3"""
        try:
            user_folder = self.get_user_folder(username)
            file_key = f"{user_folder}{file_name}"
            
            # Configurações do upload
            upload_kwargs = {
                'Bucket': self.bucket_name,
                'Key': file_key,
                'Body': file_content
            }
            
            if content_type:
                upload_kwargs['ContentType'] = content_type
            
            # Faz o upload
            response = self.s3_client.put_object(**upload_kwargs)
            
            # Obtém informações do arquivo
            file_info = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=file_key
            )
            
            return {
                'key': file_key,
                'name': file_name,
                'size': file_info['ContentLength'],
                'last_modified': file_info['LastModified'].isoformat(),
                'etag': response['ETag'].strip('"'),
                'content_type': file_info.get('ContentType', 'application/octet-stream')
            }
        except ClientError as e:
            logger.error(f"Erro ao fazer upload do arquivo: {e}")
            raise
    
    def download_file(self, username: str, file_name: str) -> Optional[Dict]:
        """Download de um arquivo do S3"""
        try:
            user_folder = self.get_user_folder(username)
            file_key = f"{user_folder}{file_name}"
            
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=file_key
            )
            
            return {
                'content': response['Body'].read(),
                'content_type': response.get('ContentType', 'application/octet-stream'),
                'size': response['ContentLength'],
                'last_modified': response['LastModified'].isoformat(),
                'etag': response['ETag'].strip('"')
            }
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.warning(f"Arquivo não encontrado: {file_key}")
                return None
            logger.error(f"Erro ao fazer download do arquivo: {e}")
            raise
    
    def delete_file(self, username: str, file_name: str) -> bool:
        """Deleta um arquivo do S3"""
        try:
            user_folder = self.get_user_folder(username)
            file_key = f"{user_folder}{file_name}"
            
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_key
            )
            
            logger.info(f"Arquivo deletado com sucesso: {file_key}")
            return True
        except ClientError as e:
            logger.error(f"Erro ao deletar arquivo: {e}")
            raise
    
    def get_file_url(self, username: str, file_name: str, expires_in: int = 3600) -> str:
        """Gera uma URL pré-assinada para download do arquivo"""
        try:
            user_folder = self.get_user_folder(username)
            file_key = f"{user_folder}{file_name}"
            
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': file_key
                },
                ExpiresIn=expires_in
            )
            
            return url
        except ClientError as e:
            logger.error(f"Erro ao gerar URL do arquivo: {e}")
            raise
    
    def get_storage_usage(self, username: str) -> Dict:
        """Calcula o uso de armazenamento do usuário"""
        try:
            files = self.list_files(username)
            total_size = sum(file['size'] for file in files)
            file_count = len(files)
            
            return {
                'total_size': total_size,
                'file_count': file_count,
                'total_size_mb': round(total_size / (1024 * 1024), 2)
            }
        except Exception as e:
            logger.error(f"Erro ao calcular uso de armazenamento: {e}")
            raise

# Instância global do gerenciador de armazenamento
storage_manager = AWSStorageManager() 