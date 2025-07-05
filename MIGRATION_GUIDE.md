# 🗄️ Guia de Configuração: Amazon RDS

## 📋 Visão Geral

Este projeto usa Amazon RDS (PostgreSQL) para armazenamento de dados de usuários, proporcionando melhor escalabilidade e performance.

## 🚀 Configuração do Ambiente

### 1. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# Configurações AWS
AWS_ACCESS_KEY_ID=sua_access_key_aqui
AWS_SECRET_ACCESS_KEY=sua_secret_key_aqui
AWS_REGION=us-east-1
AWS_S3_BUCKET=seu-bucket-s3

# Configurações do Banco (para desenvolvimento local)
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/aws_project_db

# Configurações de Segurança
SECRET_KEY=sua-chave-secreta-aqui
```

### 2. Configuração do Amazon RDS

#### Opção A: RDS Local (Docker)
```bash
docker-compose up postgres
```

#### Opção B: Amazon RDS na Nuvem
1. Crie uma instância PostgreSQL no Amazon RDS
2. Configure o Security Group para permitir conexões
3. Atualize a `DATABASE_URL` com as credenciais do RDS

### 3. Verificar Configuração

```bash
# Instalar dependências
cd backend
pip install -r requirements.txt

# Verificar se o banco está configurado corretamente
python -c "from database import create_tables; create_tables(); print('Banco configurado com sucesso!')"
```

## 🏗️ Estrutura do Banco

### Tabela `users`
```sql
CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    profile_image TEXT DEFAULT '',
    description TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 🔄 Executando o Projeto

### Com Docker (Recomendado)
```bash
docker-compose up --build
```

### Manualmente
```bash
# Terminal 1: Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

## 📊 Benefícios da Migração

1. **Escalabilidade**: Suporte a múltiplos usuários simultâneos
2. **Performance**: Consultas otimizadas com índices
3. **Integridade**: Constraints e validações do banco
4. **Backup**: Backup automático do RDS
5. **Segurança**: Isolamento de dados por usuário

## 🔧 Troubleshooting

### Problema: Erro de conexão com banco
```bash
# Verificar se o PostgreSQL está rodando
docker-compose ps

# Verificar logs
docker-compose logs postgres
```

### Problema: Banco não inicializado
```bash
# Verificar se as tabelas foram criadas
cd backend
python -c "from database import create_tables; create_tables()"
```

### Problema: Credenciais AWS
- Verifique se as variáveis de ambiente estão configuradas
- Confirme se as credenciais têm permissões para S3

## 📝 Notas Importantes

1. **Banco Vazio**: O banco inicia vazio, sem dados pré-existentes
2. **Primeiro Usuário**: Registre o primeiro usuário através da interface
3. **Backup**: Configure backup automático no Amazon RDS 