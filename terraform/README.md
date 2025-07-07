# Infraestrutura AWS com RDS

Este diretório contém a configuração da infraestrutura AWS usando Terraform para provisionar um banco de dados RDS PostgreSQL.

## 📋 Pré-requisitos

### Ferramentas Necessárias
- [Terraform](https://www.terraform.io/downloads) (>= 1.0)
- [AWS CLI](https://aws.amazon.com/cli/) configurado com suas credenciais
- Conta AWS com permissões para criar recursos RDS, VPC e Security Groups

### Configuração do AWS CLI
```bash
aws configure
```

## 🚀 Configuração e Deploy

### 1. Configurar Variáveis
```bash
# Copiar o arquivo de exemplo
cp terraform.tfvars.example terraform.tfvars

# Editar as configurações
nano terraform.tfvars
```

**Importante**: Altere principalmente:
- `db_password`: Use uma senha segura para o banco de dados
- `aws_region`: Escolha a região desejada
- `project_name`: Nome do seu projeto

### 2. Deploy da Infraestrutura

#### No Linux/macOS:
```bash
chmod +x ../deploy-infrastructure.sh
../deploy-infrastructure.sh
```

#### No Windows:
```cmd
..\deploy-infrastructure.bat
```

#### Manual:
```bash
# Entrar no diretório terraform
cd terraform

# Inicializar
terraform init

# Planejar
terraform plan

# Aplicar
terraform apply
```

## 📊 Recursos Criados

A infraestrutura criará os seguintes recursos:

- **RDS PostgreSQL Instance**: Banco de dados principal
- **DB Subnet Group**: Grupo de subnets para o RDS
- **Security Group**: Regras de firewall para o banco
- **Performance Insights**: Monitoramento de performance (habilitado)

## 🔧 Configurações do RDS

### Especificações Padrão
- **Engine**: PostgreSQL 15.4
- **Instance Class**: db.t3.micro (Free Tier eligible)
- **Storage**: 20GB (auto-scaling até 100GB)
- **Backup**: 7 dias de retenção
- **Multi-AZ**: Desabilitado (desenvolvimento)
- **Encryption**: Habilitado

### Variáveis Configuráveis
| Variável | Descrição | Padrão |
|----------|-----------|---------|
| `db_instance_class` | Classe da instância | `db.t3.micro` |
| `db_allocated_storage` | Storage inicial (GB) | `20` |
| `db_max_allocated_storage` | Storage máximo (GB) | `100` |
| `db_name` | Nome do banco | `awsproject` |
| `db_username` | Usuário do banco | `postgres` |
| `db_password` | Senha do banco | **Configurar!** |

## 🔗 Conectando a Aplicação

### 1. Obter o Endpoint
```bash
cd terraform
terraform output rds_endpoint
```

### 2. Configurar a String de Conexão
```bash
# Formato da DATABASE_URL
postgresql://username:password@endpoint:5432/database_name

# Exemplo
DATABASE_URL=postgresql://postgres:sua_senha@projeto-postgres.xxx.rds.amazonaws.com:5432/awsproject
```

### 3. Atualizar Ambiente
```bash
# No arquivo .env do backend
DATABASE_URL=postgresql://postgres:sua_senha@seu_endpoint:5432/awsproject
```

## 🚨 Segurança

### Security Group
Por padrão, o security group permite conexões de qualquer IP (0.0.0.0/0) na porta 5432. Para produção, considere:

1. **Restringir IPs**:
```hcl
cidr_blocks = ["seu.ip.específico/32"]
```

2. **Usar VPC Privada**:
- Configure uma VPC personalizada
- Use subnets privadas
- Configure NAT Gateway para acesso à internet

### Recomendações
- ✅ Use senhas fortes (mínimo 12 caracteres)
- ✅ Habilite encryption at rest (já habilitado)
- ✅ Configure backups automáticos (já configurado)
- ✅ Use SSL/TLS para conexões
- ⚠️ Restrinja access via Security Groups
- ⚠️ Configure monitoring e alertas

## 📈 Monitoramento

### Performance Insights
Já habilitado por padrão. Acesse:
1. AWS Console → RDS
2. Selecione sua instância
3. Tab "Performance Insights"

### CloudWatch Metrics
Métricas automáticas disponíveis:
- CPU Utilization
- Database Connections
- Disk IOPS
- Network Throughput

## 💰 Custos

### Free Tier
- **Instância**: db.t3.micro (750 horas/mês)
- **Storage**: 20GB SSD
- **Backup**: 20GB

### Custos Adicionais
- Storage adicional: ~$0.115/GB/mês
- Backup adicional: ~$0.095/GB/mês
- I/O requests: ~$0.20/1M requests

## 🗑️ Destruir Infraestrutura

```bash
cd terraform
terraform destroy
```

**⚠️ Cuidado**: Isso deletará permanentemente todos os dados!

## 🔍 Troubleshooting

### Erro de Conexão
1. Verificar security group
2. Verificar endpoint e porta
3. Testar conectividade:
```bash
telnet seu_endpoint 5432
```

### Erro de Credenciais
1. Verificar username/password
2. Verificar se o banco foi criado
3. Testar com cliente PostgreSQL:
```bash
psql -h seu_endpoint -p 5432 -U postgres -d awsproject
```

### Logs do RDS
1. AWS Console → RDS
2. Selecionar instância
3. Tab "Logs & events"

## 📚 Referências

- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
