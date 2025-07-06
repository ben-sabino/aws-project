# 🗄️ Guia de Conexão com RDS AWS

## 📋 Visão Geral

Este guia explica como conectar seu projeto ao **Amazon RDS PostgreSQL** que você criou na AWS.

## 🏗️ Arquitetura

```
Seu Backend → RDS PostgreSQL (Sub-rede Privada)
```

## 🚀 Passo a Passo da Conexão

### **1. Obter Informações do RDS**

Primeiro, você precisa das informações do seu RDS criado na AWS:

#### **Via Console AWS:**
1. Acesse o [Console AWS RDS](https://console.aws.amazon.com/rds/)
2. Clique em "Databases"
3. Selecione sua instância RDS
4. Anote as seguintes informações:
   - **Endpoint**: `aws-file-storage-free-db.xxxxx.us-east-1.rds.amazonaws.com`
   - **Port**: `5432`
   - **Database name**: `aws_project_db`
   - **Username**: `postgres`
   - **Password**: (a que você definiu)

#### **Via AWS CLI:**
```bash
aws rds describe-db-instances --db-instance-identifier aws-file-storage-free-db
```

### **2. Configurar Variáveis de Ambiente**

Crie um arquivo `.env` no diretório `backend/`:

```bash
cd backend
cp env.example .env
nano .env
```

**Exemplo de configuração:**
```env
# Configurações AWS
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
AWS_S3_BUCKET=aws-file-storage-free-bucket

# Configurações de Segurança
SECRET_KEY=sua-chave-secreta-muito-forte-aqui
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configurações do Banco de Dados RDS
DATABASE_URL=postgresql://postgres:SUA_SENHA@aws-file-storage-free-db.xxxxx.us-east-1.rds.amazonaws.com:5432/aws_project_db
DB_ECHO=false
```

### **3. Testar a Conexão**

Execute o script de teste para verificar se tudo está funcionando:

```bash
cd backend
python test_rds_connection.py
```

**Saída esperada:**
```
🔍 Testando conexão com RDS AWS...
==================================================
📡 Conectando ao banco: postgresql://postgres:***@aws-file-storage-free-db.xxxxx.us-east-1.rds.amazonaws.com:5432/aws_project_db
✅ Conexão com RDS estabelecida com sucesso!
✅ Tabelas criadas com sucesso!
✅ Usuário de teste criado com sucesso!
📊 Versão do PostgreSQL: PostgreSQL 15.4
📋 Tabelas criadas: users
👥 Total de usuários: 1
==================================================
🎉 Teste de conexão com RDS concluído com sucesso!
✅ O banco de dados está funcionando corretamente!
```

### **4. Executar o Backend**

Agora você pode executar o backend conectado ao RDS:

```bash
cd backend
uvicorn main:app --reload
```

## 🔒 Configurações de Segurança

### **Security Groups do RDS:**

O RDS deve estar configurado para aceitar conexões apenas do seu backend:

```hcl
# Security Group do RDS
ingress {
  from_port       = 5432
  to_port         = 5432
  protocol        = "tcp"
  security_groups = [backend_security_group_id]  # Apenas backend
}
```

### **Verificar Security Groups:**

```bash
# Obter ID do Security Group do RDS
aws rds describe-db-instances --db-instance-identifier aws-file-storage-free-db --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId'

# Verificar regras do Security Group
aws ec2 describe-security-groups --group-ids sg-xxxxx
```

## 🛠️ Comandos de Verificação

### **Testar Conexão via psql:**
```bash
# Instalar PostgreSQL client
sudo apt-get install postgresql-client  # Ubuntu/Debian
# ou
brew install postgresql  # macOS

# Conectar ao RDS
psql -h aws-file-storage-free-db.xxxxx.us-east-1.rds.amazonaws.com -U postgres -d aws_project_db
```

### **Verificar Status do RDS:**
```bash
aws rds describe-db-instances --db-instance-identifier aws-file-storage-free-db --query 'DBInstances[0].{Status:DBInstanceStatus,Endpoint:Endpoint,Port:Port}'
```

### **Verificar Logs do RDS:**
```bash
aws logs describe-log-groups --log-group-name-prefix "/aws/rds/instance/aws-file-storage-free-db"
```

## 🔧 Troubleshooting

### **Problema: "Connection refused"**

```bash
# 1. Verificar se RDS está rodando
aws rds describe-db-instances --db-instance-identifier aws-file-storage-free-db --query 'DBInstances[0].DBInstanceStatus'

# 2. Verificar Security Groups
aws ec2 describe-security-groups --group-ids sg-xxxxx

# 3. Testar conectividade
telnet aws-file-storage-free-db.xxxxx.us-east-1.rds.amazonaws.com 5432
```

### **Problema: "Authentication failed"**

```bash
# 1. Verificar credenciais
echo $DATABASE_URL

# 2. Testar com psql
psql -h ENDPOINT -U postgres -d aws_project_db
```

### **Problema: "Database does not exist"**

```bash
# 1. Conectar ao postgres padrão
psql -h ENDPOINT -U postgres -d postgres

# 2. Criar banco de dados
CREATE DATABASE aws_project_db;

# 3. Conectar ao banco criado
\c aws_project_db
```

## 📊 Monitoramento

### **Verificar Uso do RDS:**
```bash
# Verificar métricas
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name CPUUtilization \
  --dimensions Name=DBInstanceIdentifier,Value=aws-file-storage-free-db \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-31T23:59:59Z \
  --period 3600 \
  --statistics Average
```

### **Verificar Storage:**
```bash
aws rds describe-db-instances --db-instance-identifier aws-file-storage-free-db --query 'DBInstances[0].{Storage:AllocatedStorage,MaxStorage:MaxAllocatedStorage}'
```

## 🎯 URLs de Acesso

Após conectar ao RDS, você pode acessar:

- **Backend**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

## 📝 Checklist de Conexão

- [ ] RDS criado e rodando na AWS
- [ ] Endpoint do RDS anotado
- [ ] Credenciais configuradas
- [ ] Arquivo `.env` criado
- [ ] Security Groups configurados
- [ ] Teste de conexão executado
- [ ] Backend executando com RDS
- [ ] API respondendo corretamente

## 🎉 Resultado

**✅ Backend conectado ao RDS AWS com sucesso!**

- 🗄️ **Banco PostgreSQL** na nuvem
- 🔒 **Conexão segura** via Security Groups
- 📊 **Dados persistentes** no RDS
- 🚀 **Backend funcional** com autenticação

---

**⚠️ Lembre-se:** Mantenha suas credenciais seguras e nunca as commite no Git! 