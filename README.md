# AWS Project - Sistema de Gerenciamento de Arquivos

Um sistema completo de gerenciamento de arquivos na nuvem AWS, construído com React (frontend), FastAPI (backend), PostgreSQL (RDS) e integração com Amazon S3. O projeto implementa autenticação baseada em tokens JWT e utiliza infraestrutura como código com Terraform.

## 🏗️ Arquitetura do Projeto

```
.
├── backend/
│   ├── main.py          # Servidor FastAPI
│   ├── database.py      # Configuração PostgreSQL
│   ├── aws_storage.py   # Gerenciador de arquivos AWS S3
│   ├── Dockerfile       # Container do backend
│   ├── requirements.txt # Dependências Python
│   └── .env.example     # Exemplo de variáveis de ambiente
├── frontend/
│   ├── src/
│   │   ├── App.tsx      # Aplicação React
│   │   └── components/
│   │       └── FileManager.tsx # Componente de gerenciamento de arquivos
│   ├── Dockerfile       # Container do frontend
│   ├── nginx/
│   │   └── nginx.conf   # Configuração do proxy reverso
│   └── package.json     # Dependências Node.js
├── terraform/
│   ├── main.tf          # Infraestrutura AWS (RDS)
│   ├── variables.tf     # Variáveis do Terraform
│   └── README.md        # Documentação da infraestrutura
├── docker-compose.yml   # Orquestração dos containers
├── docker-compose.dev.yml # Ambiente de desenvolvimento
└── README.md
```

## 🚀 Como Executar o Projeto

### Pré-requisitos

1. **Conta AWS** com acesso ao S3 e RDS
2. **Terraform** instalado (>= 1.0)
3. **AWS CLI** configurado
4. **Docker** e **Docker Compose**

### 1. Configuração da Infraestrutura AWS

#### Deploy do RDS PostgreSQL
```bash
# 1. Configure suas credenciais AWS
aws configure

# 2. Configure o Terraform
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edite terraform.tfvars com suas configurações

# 3. Deploy da infraestrutura
# No Windows:
..\deploy-infrastructure.bat

# No Linux/macOS:
chmod +x ../deploy-infrastructure.sh
../deploy-infrastructure.sh
```

#### Configuração Manual do S3
1. **Crie um bucket S3**:
   - Acesse o console AWS S3
   - Crie um novo bucket (ex: `my-file-storage-bucket`)
   - Configure as permissões adequadas

2. **Configure as credenciais AWS**:
   - Crie um usuário IAM com permissões para S3
   - Obtenha as credenciais (Access Key ID e Secret Access Key)

### 2. Configuração do Ambiente

```bash
# Copie o arquivo de exemplo do backend
cp backend/.env.example backend/.env

# Edite o arquivo .env com suas credenciais
# DATABASE_URL (obtido do Terraform output)
DATABASE_URL=postgresql://postgres:sua_senha@seu_endpoint:5432/awsproject

# Credenciais AWS
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_REGION=us-east-1
AWS_S3_BUCKET=my-file-storage-bucket
```

### 3. Migração de Dados (Se aplicável)

Se você já tem dados no formato JSON, pode migrar para PostgreSQL:

```bash
# Execute o script de migração
cd backend
python database.py
```

### 4. Executar a Aplicação

#### Opção 1: Desenvolvimento com PostgreSQL Local

```bash
# Execute com PostgreSQL local
docker-compose -f docker-compose.dev.yml up --build
```

#### Opção 2: Usando Docker Compose (Recomendado)

```bash
# Clone o repositório (se ainda não clonou)
git clone https://github.com/ben-sabino/aws-project.git
cd aws-project

# Execute o projeto completo
docker-compose up --build
```

Isso iniciará ambos os serviços:
- **Frontend**: [http://localhost:5173](http://localhost:5173)
- **Backend**: [http://localhost:8000](http://localhost:8000)

### Opção 2: Execução Manual

#### Backend (FastAPI)

1. **Crie um ambiente virtual** (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

2. **Configure as variáveis de ambiente**:
```bash
cd backend
cp env.example .env
# Edite o arquivo .env com suas credenciais AWS
```

3. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

4. **Execute o servidor FastAPI**:
```bash
uvicorn main:app --reload
```

O backend estará disponível em [http://localhost:8000](http://localhost:8000)

#### Frontend (React)

1. **Instale as dependências**:
```bash
cd frontend
npm install
```

2. **Execute o servidor de desenvolvimento**:
```bash
npm run dev
```

O frontend estará disponível em [http://localhost:5173](http://localhost:5173)

## 🔐 Acesso ao Sistema

Você pode registrar um novo usuário diretamente na aplicação através da tela de registro.

## ✨ Funcionalidades

### 🔐 Autenticação e Autorização
- ✅ **Sistema de Login/Logout** - Autenticação segura com tokens JWT
- ✅ **Registro de Usuários** - Permite criação de novos usuários no sistema
- ✅ **Controle de Acesso** - Proteção de rotas e dados sensíveis
- ✅ **Sessões Seguras** - Gerenciamento de tokens para manter usuários logados

### 📁 Gerenciamento de Arquivos AWS
- ✅ **Upload de Arquivos** - Envio seguro para Amazon S3
- ✅ **Download de Arquivos** - Download direto dos arquivos
- ✅ **Listagem de Arquivos** - Visualização organizada dos arquivos
- ✅ **Exclusão de Arquivos** - Remoção segura de arquivos
- ✅ **Isolamento por Usuário** - Cada usuário tem sua pasta separada
- ✅ **Informações de Uso** - Estatísticas de armazenamento
- ✅ **Progresso de Upload** - Barra de progresso em tempo real
- ✅ **Validação de Tamanho** - Limite de 100MB por arquivo

### 📊 Dashboard do Usuário
- ✅ **Dashboard Personalizado** - Interface principal após autenticação
- ✅ **Menu de Navegação** - Acesso fácil a todas as funcionalidades
- ✅ **Gestão de Perfil** - Edição completa das informações do usuário

## 👤 Perfil de Usuário

O sistema gerencia as seguintes informações do usuário:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| **Nome Completo** | String | Nome completo do usuário |
| **Username** | String | Nome de usuário único para login |
| **Email** | String | Endereço de email válido |
| **Password** | String | Senha criptografada |
| **Imagem de Perfil** | URL | Foto do perfil do usuário |
| **Descrição** | Text | Biografia ou descrição pessoal |
| **Data de Criação** | DateTime | Data e hora de criação da conta |

### Funcionalidades de Perfil
- ✅ **Edição Completa** - Todos os campos podem ser editados
- ✅ **Validação de Dados** - Verificação de formato de email e senha
- ✅ **Inserção de Imagem** - Suporte a formatos JPG, PNG e GIF
- ✅ **Alteração Segura** - Senha atual necessária para alterações críticas

### 🛠️ Recursos Técnicos
- ✅ **Interface Responsiva** - Baseada em Material-UI
- ✅ **Rotas Protegidas** - Controle de acesso por autenticação
- ✅ **API RESTful** - Endpoints organizados e documentados
- ✅ **Containerização** - Suporte ao Docker para implantação fácil
- ✅ **Integração AWS S3** - Armazenamento seguro na nuvem

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e rápido para Python
- **JWT** - JSON Web Tokens para autenticação
- **Boto3** - SDK AWS para Python
- **Python 3.x** - Linguagem de programação

### Frontend
- **React** - Biblioteca JavaScript para interfaces de usuário
- **TypeScript** - Superset tipado do JavaScript
- **Material-UI** - Biblioteca de componentes React
- **Vite** - Ferramenta de build rápida

### Cloud
- **Amazon S3** - Armazenamento de objetos na nuvem
- **AWS IAM** - Gerenciamento de identidade e acesso

### DevOps
- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers

## 📝 Endpoints da API

O backend expõe os seguintes endpoints:

### Autenticação
- `POST /api/register` - Registro de novos usuários
- `POST /api/token` - Autenticação de usuário

### Perfil do Usuário
- `GET /api/users/me` - Obter informações do perfil (requer token)
- `PUT /api/users/me` - Atualizar informações do perfil (requer token)
- `PUT /api/users/me/password` - Alterar senha (requer token)

### Gerenciamento de Arquivos
- `GET /api/files` - Listar arquivos do usuário (requer token)
- `POST /api/files/upload` - Upload de arquivo (requer token)
- `GET /api/files/download/{file_name}` - Download de arquivo (requer token)
- `DELETE /api/files/{file_name}` - Deletar arquivo (requer token)
- `GET /api/files/{file_name}/url` - Gerar URL pré-assinada (requer token)
- `GET /api/storage/usage` - Estatísticas de uso (requer token)

### Sistema
- `GET /docs` - Documentação automática da API (Swagger)
- `GET /health` - Status de saúde da aplicação

## 🔧 Desenvolvimento

### Estrutura do Backend
- `main.py`: Contém toda a lógica do servidor FastAPI, incluindo rotas de autenticação e gerenciamento de arquivos
- `aws_storage.py`: Gerenciador de arquivos AWS S3 com todas as operações de CRUD

### Estrutura do Frontend
- `src/App.tsx`: Componente principal da aplicação React com lógica de login e interface
- `src/components/FileManager.tsx`: Componente especializado para gerenciamento de arquivos

## 📦 Scripts Disponíveis

### Frontend
```bash
npm run dev     # Inicia o servidor de desenvolvimento
npm run build   # Constrói a aplicação para produção
npm run preview # Visualiza a build de produção
```

### Backend
```bash
uvicorn main:app --reload          # Servidor de desenvolvimento
uvicorn main:app --host 0.0.0.0    # Servidor para produção
```

## 🐳 Docker

### Construir imagens individualmente
```bash
# Backend
cd backend
docker build -t aws-project-backend .

# Frontend
cd frontend
docker build -t aws-project-frontend .
```

### Executar containers individualmente
```bash
# Backend
docker run -p 8000:8000 aws-project-backend
```

## 🔒 Segurança

### AWS S3
- Cada usuário tem sua pasta isolada no S3
- URLs pré-assinadas para download seguro
- Validação de tamanho de arquivo (máximo 100MB)
- Controle de acesso baseado em tokens JWT

### Autenticação
- Tokens JWT com expiração configurável
- Senhas criptografadas com bcrypt
- Middleware CORS configurado adequadamente

## 💰 Custos AWS

O sistema utiliza os seguintes serviços AWS:
- **S3**: Armazenamento de objetos (custo baseado no uso)
- **IAM**: Gerenciamento de identidade (gratuito)

### Estimativa de Custos
- **S3 Standard**: ~$0.023 por GB/mês
- **Transferência de dados**: ~$0.09 por GB (saída)
- **Operações**: ~$0.0004 por 1.000 requisições

Para uso pessoal ou pequenas empresas, os custos são mínimos.

## 🚀 Deploy em Produção

### Configuração de Produção
1. Configure um bucket S3 dedicado
2. Configure as variáveis de ambiente de produção
3. Use HTTPS em produção
4. Configure um domínio personalizado
5. Configure monitoramento e logs

### Variáveis de Ambiente de Produção
```bash
AWS_ACCESS_KEY_ID=your_production_access_key
AWS_SECRET_ACCESS_KEY=your_production_secret_key
AWS_REGION=us-east-1
AWS_S3_BUCKET=your-production-bucket
SECRET_KEY=your-production-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique se todas as dependências estão instaladas
2. Certifique-se de que as portas 3000, 5173 e 8000 estão livres
3. Para problemas com Docker, tente `docker-compose down` e depois `docker-compose up --build`
4. Abra uma issue no repositório do GitHub

---

**Desenvolvido por:** [ben-sabino](https://github.com/ben-sabino), [caioburton](https://github.com/CaioBurton) e [GuilberthBruno](https://github.com/GuilberthBruno)
