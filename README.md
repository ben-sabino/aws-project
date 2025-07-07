# AWS Project - Sistema de Gerenciamento de Arquivos

Um sistema de login simples construído com React (frontend) e FastAPI (backend), implementando autenticação baseada em tokens JWT.

## 🏗️ Arquitetura do Projeto

```
.
├── backend/
│   ├── main.py          # Servidor FastAPI
│   ├── Dockerfile       # Container do backend
│   └── requirements.txt # Dependências Python
├── frontend/
│   ├── src/
│   │   └── App.tsx      # Aplicação React
│   ├── Dockerfile       # Container do frontend
│   └── package.json     # Dependências Node.js
├── docker-compose.yml   # Orquestração dos containers
└── README.md
```

## 🚀 Como Executar o Projeto

### Opção 1: Usando Docker Compose (Recomendado)

A maneira mais fácil de executar a aplicação é usando Docker Compose:

```bash
# Clone o repositório
git clone https://github.com/ben-sabino/aws-project.git
cd aws-project

# Execute o projeto
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

2. **Instale as dependências**:
```bash
cd backend
pip install -r requirements.txt
```

3. **Execute o servidor FastAPI**:
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

### � Gerenciamento de Arquivos
- ✅ **Upload de Arquivos** - Envio seguro de arquivos para o servidor
- ✅ **Listagem de Arquivos** - Visualização de todos os arquivos do usuário
- ✅ **Pesquisa de Arquivos** - Busca por nome de arquivo
- ✅ **Download de Arquivos** - Download seguro dos arquivos enviados
- ✅ **Exclusão de Arquivos** - Remoção de arquivos não desejados
- ✅ **Informações Detalhadas** - Tamanho, tipo e data de upload

### �📊 Dashboard do Usuário
- ✅ **Dashboard Personalizado** - Interface principal após autenticação
- ✅ **Menu de Navegação** - Acesso fácil a todas as funcionalidades
- ✅ **Gestão de Perfil** - Edição completa das informações do usuário
- ✅ **Resumo de Arquivos** - Estatísticas dos arquivos enviados

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

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e rápido para Python
- **JWT** - JSON Web Tokens para autenticação
- **Python 3.x** - Linguagem de programação

### Frontend
- **React** - Biblioteca JavaScript para interfaces de usuário
- **TypeScript** - Superset tipado do JavaScript
- **Material-UI** - Biblioteca de componentes React
- **Vite** - Ferramenta de build rápida

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
- `POST /api/files/upload` - Upload de arquivo (requer token)
- `GET /api/files` - Listar arquivos do usuário (requer token)
- `GET /api/files/{file_id}` - Download de arquivo específico (requer token)
- `DELETE /api/files/{file_id}` - Excluir arquivo (requer token)

### Sistema
- `GET /docs` - Documentação automática da API (Swagger)
- `GET /uploads/{filename}` - Servir arquivos estáticos

## 🔧 Desenvolvimento

### Estrutura do Backend
- `main.py`: Contém toda a lógica do servidor FastAPI, incluindo rotas de autenticação e middleware de CORS

### Estrutura do Frontend
- `src/App.tsx`: Componente principal da aplicação React com lógica de login e interface

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

# Frontend  
docker run -p 5173:5173 aws-project-frontend
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
