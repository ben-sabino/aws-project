import { useState, useEffect } from 'react'
import type { FormEvent, ChangeEvent } from 'react'
import { Container, Box, TextField, Button, Typography, Alert, Tabs, Tab } from '@mui/material'
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom'

import axios from 'axios'

// Configuração global do axios
axios.defaults.baseURL = 'http://localhost:8000'
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

interface LoginResponse {
  access_token: string;
  token_type: string;
}

interface UserResponse {
  username: string;
}

interface RegisterResponse {
  access_token: string;
  token_type: string;
  username: string;
}

function HomePage() {
  const navigate = useNavigate()

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 8, textAlign: 'center' }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Bem-vindo ao Sistema de Armazenamento de Arquivos
        </Typography>
        <Typography variant="h6" component="h2" gutterBottom sx={{ mb: 4 }}>
          Uma solução simples e segura para armazenar seus arquivos na nuvem
        </Typography>
        <Typography variant="body1" sx={{ mb: 4 }}>
          Com nosso sistema, você pode fazer upload, organizar e compartilhar seus arquivos
          de forma segura e eficiente. Mantenha seus documentos importantes sempre acessíveis
          e protegidos.
        </Typography>
        <Button
          variant="contained"
          size="large"
          onClick={() => navigate('/login')}
          sx={{ mt: 2 }}
        >
          Começar Agora
        </Button>
      </Box>
    </Container>
  )
}

function Dashboard() {
  const navigate = useNavigate()
  const username = localStorage.getItem('username')

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      navigate('/login')
    }
  }, [navigate])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    navigate('/login')
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, width: '100%' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Typography variant="h4">
            Olá, {username}!
          </Typography>
          <Button
            onClick={handleLogout}
            variant="outlined"
            color="primary"
          >
            Sair
          </Button>
        </Box>
        <Typography variant="body1" sx={{ mb: 2 }}>
          Bem-vindo ao seu painel de controle. Aqui você pode gerenciar seus arquivos.
        </Typography>
      </Box>
    </Container>
  )
}

function AuthForm() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [activeTab, setActiveTab] = useState(0)
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      navigate('/dashboard')
    }
  }, [navigate])

  const handleLogin = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    try {
      const formData = new FormData()
      formData.append('username', username)
      formData.append('password', password)

      await axios.post<RegisterResponse>('/register', {        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      localStorage.setItem('token', response.data.access_token)

      // Fetch user data
      const userResponse = await axios.get<UserResponse>('/users/me', {
        headers: {
          Authorization: `Bearer ${response.data.access_token}`,
        },
      })
      
      localStorage.setItem('username', userResponse.data.username)
      navigate('/dashboard', { replace: true })
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Falha no login. Por favor, verifique suas credenciais.')
      console.error('Login error:', err)
    }
  }

  const handleRegister = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    try {
      const response = await axios.post<RegisterResponse>('/register', {
        username,
        password,
      })

      setSuccess('Cadastro realizado com sucesso! Você já pode fazer login.')
      setUsername('')
      setPassword('')
      setActiveTab(0)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Falha no cadastro. Por favor, tente novamente.')
      console.error('Registration error:', err)
    }
  }

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue)
    setError('')
    setSuccess('')
  }

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography component="h1" variant="h5" sx={{ mb: 3 }}>
          {activeTab === 0 ? 'Login' : 'Criar Conta'}
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2, width: '100%' }}>
            {error}
          </Alert>
        )}

        {success && (
          <Alert severity="success" sx={{ mb: 2, width: '100%' }}>
            {success}
          </Alert>
        )}

        <Box sx={{ borderBottom: 1, borderColor: 'divider', width: '100%', mb: 3 }}>
          <Tabs value={activeTab} onChange={handleTabChange} centered>
            <Tab label="Login" />
            <Tab label="Criar Conta" />
          </Tabs>
        </Box>

        <Box
          component="form"
          onSubmit={activeTab === 0 ? handleLogin : handleRegister}
          sx={{ mt: 1, width: '100%' }}
        >
          <TextField
            margin="normal"
            required
            fullWidth
            label="Usuário"
            value={username}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setUsername(e.target.value)}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            label="Senha"
            type="password"
            value={password}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            {activeTab === 0 ? 'Entrar' : 'Criar Conta'}
          </Button>
        </Box>
      </Box>
    </Container>
  )
}

function App() {
  return (
    <Box sx={{ 
      minHeight: '100vh',
      backgroundColor: '#ffffff',
      display: 'flex',
      flexDirection: 'column'
    }}>
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<AuthForm />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </Router>
    </Box>
  )
}

export default App
