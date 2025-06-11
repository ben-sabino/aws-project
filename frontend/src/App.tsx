import React, { useState, useEffect } from 'react'
import type { FormEvent, ChangeEvent } from 'react'
import { 
  Container, 
  Box, 
  TextField, 
  Button, 
  Typography, 
  Alert, 
  Tabs, 
  Tab,
  Card,
  CardContent,
  Avatar,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Grid,
  AppBar,
  Toolbar,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material'
import {
  Dashboard as DashboardIcon,
  Person as PersonIcon,
  Settings as SettingsIcon,
  Edit as EditIcon,
  Lock as LockIcon,
  Menu as MenuIcon,
  ExitToApp as ExitToAppIcon
} from '@mui/icons-material'
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom'

import axios from 'axios'

// Configuração global do axios
axios.defaults.baseURL = '/api'
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
  full_name: string;
  email: string;
  profile_image: string;
  description: string;
  created_at: string;
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
        <Typography variant="h3" component="h1" gutterBottom sx={{ color: 'black' }}>
          Bem-vindo ao Sistema de Armazenamento de Arquivos
        </Typography>
        <Typography variant="h6" component="h2" gutterBottom sx={{ mb: 4, color: 'black' }}>
          Uma solução simples e segura para armazenar seus arquivos na nuvem
        </Typography>
        <Typography variant="body1" sx={{ mb: 4, color: 'black' }}>
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
  const [user, setUser] = useState<UserResponse | null>(null)
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [selectedMenuItem, setSelectedMenuItem] = useState('dashboard')
  const [editDialogOpen, setEditDialogOpen] = useState(false)
  const [passwordDialogOpen, setPasswordDialogOpen] = useState(false)
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    description: '',
    profile_image: ''
  })
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      navigate('/login')
      return
    }

    // Fetch user data
    fetchUserData()
  }, [navigate])

  const fetchUserData = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get<UserResponse>('/users/me', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      setUser(response.data)
      setFormData({
        full_name: response.data.full_name,
        email: response.data.email,
        description: response.data.description,
        profile_image: response.data.profile_image
      })
    } catch (err) {
      console.error('Error fetching user data:', err)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    navigate('/login')
  }

  const handleUpdateProfile = async () => {
    try {
      setError('')
      setSuccess('')
      const token = localStorage.getItem('token')
      await axios.put('/users/me', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      setSuccess('Perfil atualizado com sucesso!')
      setEditDialogOpen(false)
      fetchUserData()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao atualizar perfil')
    }
  }

  const handleUpdatePassword = async () => {
    try {
      setError('')
      setSuccess('')
      
      if (passwordData.new_password !== passwordData.confirm_password) {
        setError('As senhas não coincidem')
        return
      }

      const token = localStorage.getItem('token')
      await axios.put('/users/me/password', {
        current_password: passwordData.current_password,
        new_password: passwordData.new_password
      }, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      setSuccess('Senha alterada com sucesso!')
      setPasswordDialogOpen(false)
      setPasswordData({ current_password: '', new_password: '', confirm_password: '' })
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao alterar senha')
    }
  }

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: <DashboardIcon /> },
    { id: 'profile', label: 'Perfil', icon: <PersonIcon /> },
    { id: 'settings', label: 'Configurações', icon: <SettingsIcon /> },
  ]

  const renderContent = () => {
    switch (selectedMenuItem) {
      case 'dashboard':
        return (
          <Box>
            <Typography variant="h4" sx={{ mb: 3, color: 'black' }}>
              Dashboard
            </Typography>            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" sx={{ color: 'black' }}>
                      Bem-vindo, {user?.full_name || user?.username}!
                    </Typography>
                    <Typography variant="body2" sx={{ mt: 1, color: 'black' }}>
                      Usuário desde: {user?.created_at ? new Date(user.created_at).toLocaleDateString() : ''}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" sx={{ color: 'black' }}>
                      Ações Rápidas
                    </Typography>
                    <Box sx={{ mt: 2 }}>
                      <Button
                        variant="outlined"
                        startIcon={<EditIcon />}
                        onClick={() => {
                          setSelectedMenuItem('profile')
                          setEditDialogOpen(true)
                        }}
                        sx={{ mr: 1, mb: 1 }}
                      >
                        Editar Perfil
                      </Button>
                      <Button
                        variant="outlined"
                        startIcon={<LockIcon />}
                        onClick={() => setPasswordDialogOpen(true)}
                        sx={{ mb: 1 }}
                      >
                        Alterar Senha
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Box>
        )
      case 'profile':
        return (
          <Box>
            <Typography variant="h4" sx={{ mb: 3, color: 'black' }}>
              Meu Perfil
            </Typography>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                  <Avatar
                    src={user?.profile_image}
                    sx={{ width: 80, height: 80, mr: 3 }}
                  >
                    {user?.full_name?.charAt(0) || user?.username?.charAt(0)}
                  </Avatar>
                  <Box>
                    <Typography variant="h5" sx={{ color: 'black' }}>
                      {user?.full_name || user?.username}
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'gray' }}>
                      @{user?.username}
                    </Typography>
                  </Box>
                </Box>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 'bold', color: 'black' }}>
                      Email:
                    </Typography>
                    <Typography variant="body1" sx={{ color: 'black' }}>
                      {user?.email}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 'bold', color: 'black' }}>
                      Membro desde:
                    </Typography>
                    <Typography variant="body1" sx={{ color: 'black' }}>
                      {user?.created_at ? new Date(user.created_at).toLocaleDateString() : ''}
                    </Typography>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 'bold', color: 'black' }}>
                      Descrição:
                    </Typography>
                    <Typography variant="body1" sx={{ color: 'black' }}>
                      {user?.description || 'Nenhuma descrição disponível'}
                    </Typography>
                  </Grid>
                </Grid>
                <Box sx={{ mt: 3 }}>
                  <Button
                    variant="contained"
                    startIcon={<EditIcon />}
                    onClick={() => setEditDialogOpen(true)}
                    sx={{ mr: 2 }}
                  >
                    Editar Perfil
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<LockIcon />}
                    onClick={() => setPasswordDialogOpen(true)}
                  >
                    Alterar Senha
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Box>
        )
      case 'settings':
        return (
          <Box>
            <Typography variant="h4" sx={{ mb: 3, color: 'black' }}>
              Configurações
            </Typography>
            <Card>
              <CardContent>
                <Typography variant="body1" sx={{ color: 'black' }}>
                  Configurações do sistema em desenvolvimento...
                </Typography>
              </CardContent>
            </Card>
          </Box>
        )
      default:
        return null
    }
  }

  if (!user) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <Typography sx={{ color: 'black' }}>Carregando...</Typography>
      </Box>
    )
  }

  return (
    <Box sx={{ display: 'flex' }}>
      {/* AppBar */}
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={() => setDrawerOpen(!drawerOpen)}
            edge="start"
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            Sistema de Arquivos
          </Typography>
          <Button color="inherit" onClick={handleLogout} startIcon={<ExitToAppIcon />}>
            Sair
          </Button>
        </Toolbar>
      </AppBar>

      {/* Drawer */}
      <Drawer
        variant="temporary"
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        sx={{
          width: 240,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: 240,
            boxSizing: 'border-box',
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            {menuItems.map((item) => (
              <ListItem
                key={item.id}
                onClick={() => {
                  setSelectedMenuItem(item.id)
                  setDrawerOpen(false)
                }}
                sx={{
                  cursor: 'pointer',
                  backgroundColor: selectedMenuItem === item.id ? 'rgba(0, 0, 0, 0.08)' : 'transparent'
                }}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.label} />
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>

      {/* Main content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          bgcolor: 'background.default',
          p: 3,
        }}
      >
        <Toolbar />
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        {success && (
          <Alert severity="success" sx={{ mb: 2 }}>
            {success}
          </Alert>
        )}
        {renderContent()}
      </Box>

      {/* Edit Profile Dialog */}
      <Dialog open={editDialogOpen} onClose={() => setEditDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ color: 'black' }}>Editar Perfil</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Nome Completo"
            fullWidth
            variant="outlined"
            value={formData.full_name}
            onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Email"
            type="email"
            fullWidth
            variant="outlined"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Descrição"
            fullWidth
            multiline
            rows={3}
            variant="outlined"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="URL da Imagem do Perfil"
            fullWidth
            variant="outlined"
            value={formData.profile_image}
            onChange={(e) => setFormData({ ...formData, profile_image: e.target.value })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditDialogOpen(false)}>Cancelar</Button>
          <Button onClick={handleUpdateProfile} variant="contained">Salvar</Button>
        </DialogActions>
      </Dialog>

      {/* Change Password Dialog */}
      <Dialog open={passwordDialogOpen} onClose={() => setPasswordDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ color: 'black' }}>Alterar Senha</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Senha Atual"
            type="password"
            fullWidth
            variant="outlined"
            value={passwordData.current_password}
            onChange={(e) => setPasswordData({ ...passwordData, current_password: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Nova Senha"
            type="password"
            fullWidth
            variant="outlined"
            value={passwordData.new_password}
            onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Confirmar Nova Senha"
            type="password"
            fullWidth
            variant="outlined"
            value={passwordData.confirm_password}
            onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPasswordDialogOpen(false)}>Cancelar</Button>
          <Button onClick={handleUpdatePassword} variant="contained">Alterar Senha</Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}

function AuthForm() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [description, setDescription] = useState('')
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
      // Para login com usuário e senha, o FastAPI geralmente espera 'x-www-form-urlencoded'
      // A classe URLSearchParams é perfeita para isso.
      const formData = new URLSearchParams()
      formData.append('username', username)
      formData.append('password', password)

      // 1. Chame o endpoint correto para login (ex: /token)
      // 2. Guarde a resposta em uma variável (ex: loginResponse)
      const loginResponse = await axios.post<LoginResponse>('/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      })

      // 3. Use a variável da resposta para obter o token
      const token = loginResponse.data.access_token
      localStorage.setItem('token', token)

      // 4. Use a mesma variável 'token' para a próxima chamada
      const userResponse = await axios.get<UserResponse>('/users/me', {
        headers: {
          Authorization: `Bearer ${token}`,
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
      await axios.post<RegisterResponse>('/register', {
        username,
        password,
        full_name: fullName,
        email,
        description,
      })

      setSuccess('Cadastro realizado com sucesso! Você já pode fazer login.')
      setUsername('')
      setPassword('')
      setFullName('')
      setEmail('')
      setDescription('')
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
    <Container maxWidth="sm">      <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography component="h1" variant="h5" sx={{ mb: 3, color: 'black' }}>
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
          
          {activeTab === 1 && (
            <>
              <TextField
                margin="normal"
                required
                fullWidth
                label="Nome Completo"
                value={fullName}
                onChange={(e: ChangeEvent<HTMLInputElement>) => setFullName(e.target.value)}
              />
              <TextField
                margin="normal"
                required
                fullWidth
                label="Email"
                type="email"
                value={email}
                onChange={(e: ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
              />
              <TextField
                margin="normal"
                fullWidth
                label="Descrição (opcional)"
                multiline
                rows={2}
                value={description}
                onChange={(e: ChangeEvent<HTMLInputElement>) => setDescription(e.target.value)}
              />
            </>
          )}
          
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
