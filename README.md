# React + FastAPI Login System

This is a simple login system built with React (frontend) and FastAPI (backend). The system implements token-based authentication.

## Project Structure

```
.
├── backend/
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   └── App.tsx
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Running with Docker (Recommended)

The easiest way to run the application is using Docker Compose:

```bash
docker-compose up --build
```

This will start both the frontend and backend services:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000

## Manual Setup and Running

### Backend Setup

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will run on http://localhost:8000

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```
   The frontend will run on http://localhost:5173

## Test Credentials

- Username: testuser
- Password: testpass

## Features

- User authentication with JWT tokens
- Material-UI based responsive interface
- Protected routes
- Token-based API authentication
- Docker support for easy deployment 