#!/usr/bin/env python3
"""
Script de teste para verificar a integração com AWS S3
Execute este script para testar se as credenciais AWS estão configuradas corretamente
"""

import os
import sys
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv

load_dotenv()

def test_aws_credentials():
    """Testa se as credenciais AWS estão configuradas"""
    print("🔍 Testando credenciais AWS...")
    
    try:
        # Tenta criar um cliente S3
        s3_client = boto3.client('s3')
        
        # Lista os buckets disponíveis
        response = s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        
        print("✅ Credenciais AWS configuradas com sucesso!")
        print(f"📦 Buckets disponíveis: {buckets}")
        
        return True
    except NoCredentialsError:
        print("❌ Credenciais AWS não encontradas!")
        print("💡 Configure as variáveis de ambiente:")
        print("   AWS_ACCESS_KEY_ID=your_access_key_id")
        print("   AWS_SECRET_ACCESS_KEY=your_secret_access_key")
        print("   AWS_REGION=us-east-1")
        return False
    except Exception as e:
        print(f"❌ Erro ao conectar com AWS: {e}")
        return False

def test_s3_bucket(bucket_name):
    """Testa se o bucket S3 existe e está acessível"""
    print(f"\n🔍 Testando bucket S3: {bucket_name}")
    
    try:
        s3_client = boto3.client('s3')
        
        # Verifica se o bucket existe
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' existe e está acessível!")
        
        # Lista alguns objetos (máximo 10)
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            MaxKeys=10
        )
        
        if 'Contents' in response:
            print(f"📁 Encontrados {len(response['Contents'])} objetos no bucket")
            for obj in response['Contents'][:5]:  # Mostra apenas os primeiros 5
                print(f"   - {obj['Key']} ({obj['Size']} bytes)")
        else:
            print("📁 Bucket está vazio")
        
        return True
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"❌ Bucket '{bucket_name}' não encontrado!")
            print("💡 Crie o bucket no console AWS S3")
        elif error_code == '403':
            print(f"❌ Acesso negado ao bucket '{bucket_name}'!")
            print("💡 Verifique as permissões IAM")
        else:
            print(f"❌ Erro ao acessar bucket: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_file_operations(bucket_name):
    """Testa operações básicas de arquivo no S3"""
    print(f"\n🔍 Testando operações de arquivo no bucket: {bucket_name}")
    
    try:
        s3_client = boto3.client('s3')
        test_key = 'test-file.txt'
        test_content = b'Hello, AWS S3! This is a test file.'
        
        # Upload de teste
        print("📤 Fazendo upload de arquivo de teste...")
        s3_client.put_object(
            Bucket=bucket_name,
            Key=test_key,
            Body=test_content,
            ContentType='text/plain'
        )
        print("✅ Upload realizado com sucesso!")
        
        # Download de teste
        print("📥 Fazendo download de arquivo de teste...")
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=test_key
        )
        downloaded_content = response['Body'].read()
        
        if downloaded_content == test_content:
            print("✅ Download realizado com sucesso!")
        else:
            print("❌ Conteúdo do download não corresponde ao original!")
            return False
        
        # Deletar arquivo de teste
        print("🗑️ Deletando arquivo de teste...")
        s3_client.delete_object(
            Bucket=bucket_name,
            Key=test_key
        )
        print("✅ Arquivo de teste deletado com sucesso!")
        
        return True
    except Exception as e:
        print(f"❌ Erro durante operações de arquivo: {e}")
        return False

def main():
    """Função principal do script de teste"""
    print("🚀 Iniciando testes de integração AWS S3")
    print("=" * 50)
    
    # Verifica variáveis de ambiente
    bucket_name = os.getenv('AWS_S3_BUCKET', 'my-file-storage-bucket')
    region = os.getenv('AWS_REGION', 'us-east-1')
    
    print(f"📋 Configurações:")
    print(f"   Bucket: {bucket_name}")
    print(f"   Região: {region}")
    print(f"   Access Key ID: {'✅ Configurado' if os.getenv('AWS_ACCESS_KEY_ID') else '❌ Não configurado'}")
    print(f"   Secret Access Key: {'✅ Configurado' if os.getenv('AWS_SECRET_ACCESS_KEY') else '❌ Não configurado'}")
    
    # Testa credenciais
    if not test_aws_credentials():
        print("\n❌ Falha nos testes. Configure as credenciais AWS primeiro.")
        sys.exit(1)
    
    # Testa bucket
    if not test_s3_bucket(bucket_name):
        print("\n❌ Falha nos testes. Verifique o bucket S3.")
        sys.exit(1)
    
    # Testa operações de arquivo
    if not test_file_operations(bucket_name):
        print("\n❌ Falha nos testes. Verifique as permissões do bucket.")
        sys.exit(1)
    
    print("\n🎉 Todos os testes passaram com sucesso!")
    print("✅ O sistema está pronto para uso com AWS S3!")
    print("\n💡 Próximos passos:")
    print("   1. Execute o backend: uvicorn main:app --reload")
    print("   2. Execute o frontend: npm run dev")
    print("   3. Acesse: http://localhost:5173")

if __name__ == "__main__":
    main() 