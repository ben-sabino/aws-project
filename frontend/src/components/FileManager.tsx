import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  LinearProgress,
  Alert,
  Chip,
  Tooltip,
  CircularProgress
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  Download as DownloadIcon,
  Delete as DeleteIcon,
  Refresh as RefreshIcon,
  Storage as StorageIcon
} from '@mui/icons-material';
import axios from 'axios';

interface FileInfo {
  key: string;
  name: string;
  size: number;
  last_modified: string;
  etag: string;
  content_type?: string;
}

interface StorageUsage {
  total_size: number;
  file_count: number;
  total_size_mb: number;
}

const FileManager: React.FC = () => {
  const [files, setFiles] = useState<FileInfo[]>([]);
  const [storageUsage, setStorageUsage] = useState<StorageUsage | null>(null);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [fileToDelete, setFileToDelete] = useState<FileInfo | null>(null);

  useEffect(() => {
    fetchFiles();
    fetchStorageUsage();
  }, []);

  const fetchFiles = async () => {
    try {
      setLoading(true);
      setError('');
      const token = localStorage.getItem('token');
      const response = await axios.get<FileInfo[]>('/files', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setFiles(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao carregar arquivos');
    } finally {
      setLoading(false);
    }
  };

  const fetchStorageUsage = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get<StorageUsage>('/storage/usage', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStorageUsage(response.data);
    } catch (err: any) {
      console.error('Erro ao carregar uso de armazenamento:', err);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validar tamanho do arquivo (100MB)
    if (file.size > 100 * 1024 * 1024) {
      setError('Arquivo muito grande. Máximo 100MB');
      return;
    }

    try {
      setUploading(true);
      setUploadProgress(0);
      setError('');
      setSuccess('');

      const formData = new FormData();
      formData.append('file', file);

      const token = localStorage.getItem('token');
      await axios.post('/files/upload', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });

      setSuccess('Arquivo enviado com sucesso!');
      fetchFiles();
      fetchStorageUsage();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao fazer upload do arquivo');
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  const handleDownload = async (file: FileInfo) => {
    try {
      setError('');
      const token = localStorage.getItem('token');
      const response = await axios.get(`/files/download/${encodeURIComponent(file.name)}`, {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob'
      });

      // Criar link para download
      const url = window.URL.createObjectURL(new Blob([response.data as BlobPart]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', file.name);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao fazer download do arquivo');
    }
  };

  const handleDeleteClick = (file: FileInfo) => {
    setFileToDelete(file);
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (!fileToDelete) return;

    try {
      setError('');
      const token = localStorage.getItem('token');
      await axios.delete(`/files/${encodeURIComponent(fileToDelete.name)}`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setSuccess('Arquivo deletado com sucesso!');
      fetchFiles();
      fetchStorageUsage();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao deletar arquivo');
    } finally {
      setDeleteDialogOpen(false);
      setFileToDelete(null);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleString('pt-BR');
  };

  const getFileIcon = (fileName: string) => {
    const extension = fileName.split('.').pop()?.toLowerCase();
    switch (extension) {
      case 'pdf':
        return '📄';
      case 'doc':
      case 'docx':
        return '📝';
      case 'xls':
      case 'xlsx':
        return '📊';
      case 'jpg':
      case 'jpeg':
      case 'png':
      case 'gif':
        return '🖼️';
      case 'mp4':
      case 'avi':
      case 'mov':
        return '🎥';
      case 'mp3':
      case 'wav':
        return '🎵';
      default:
        return '📁';
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Gerenciador de Arquivos
        </Typography>
        <Box>
          <input
            accept="*/*"
            style={{ display: 'none' }}
            id="file-upload"
            type="file"
            onChange={handleFileUpload}
            disabled={uploading}
          />
          <label htmlFor="file-upload">
            <Button
              variant="contained"
              component="span"
              startIcon={<UploadIcon />}
              disabled={uploading}
              sx={{ mr: 1 }}
            >
              {uploading ? 'Enviando...' : 'Enviar Arquivo'}
            </Button>
          </label>
          <IconButton onClick={fetchFiles} disabled={loading}>
            <RefreshIcon />
          </IconButton>
        </Box>
      </Box>

      {/* Storage Usage */}
      {storageUsage && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <StorageIcon sx={{ mr: 1 }} />
              <Typography variant="h6">Uso de Armazenamento</Typography>
            </Box>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={4}>
                <Typography variant="body2" color="text.secondary">
                  Total de Arquivos
                </Typography>
                <Typography variant="h6">{storageUsage.file_count}</Typography>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Typography variant="body2" color="text.secondary">
                  Tamanho Total
                </Typography>
                <Typography variant="h6">{formatFileSize(storageUsage.total_size)}</Typography>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Typography variant="body2" color="text.secondary">
                  Espaço Usado
                </Typography>
                <Typography variant="h6">{storageUsage.total_size_mb} MB</Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}

      {/* Upload Progress */}
      {uploading && (
        <Box sx={{ mb: 2 }}>
          <Typography variant="body2" sx={{ mb: 1 }}>
            Enviando arquivo... {uploadProgress}%
          </Typography>
          <LinearProgress variant="determinate" value={uploadProgress} />
        </Box>
      )}

      {/* Alerts */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}
      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess('')}>
          {success}
        </Alert>
      )}

      {/* Files Table */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Seus Arquivos ({files.length})
          </Typography>
          
          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
              <CircularProgress />
            </Box>
          ) : files.length === 0 ? (
            <Box sx={{ textAlign: 'center', p: 3 }}>
              <Typography variant="body1" color="text.secondary">
                Nenhum arquivo encontrado. Faça upload do seu primeiro arquivo!
              </Typography>
            </Box>
          ) : (
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Arquivo</TableCell>
                    <TableCell>Tamanho</TableCell>
                    <TableCell>Modificado</TableCell>
                    <TableCell align="center">Ações</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {files.map((file) => (
                    <TableRow key={file.key}>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <Typography sx={{ mr: 1, fontSize: '1.2em' }}>
                            {getFileIcon(file.name)}
                          </Typography>
                          <Box>
                            <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                              {file.name}
                            </Typography>
                            {file.content_type && (
                              <Chip
                                label={file.content_type}
                                size="small"
                                variant="outlined"
                                sx={{ mt: 0.5 }}
                              />
                            )}
                          </Box>
                        </Box>
                      </TableCell>
                      <TableCell>{formatFileSize(file.size)}</TableCell>
                      <TableCell>{formatDate(file.last_modified)}</TableCell>
                      <TableCell align="center">
                        <Tooltip title="Download">
                          <IconButton
                            onClick={() => handleDownload(file)}
                            color="primary"
                            size="small"
                          >
                            <DownloadIcon />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Deletar">
                          <IconButton
                            onClick={() => handleDeleteClick(file)}
                            color="error"
                            size="small"
                          >
                            <DeleteIcon />
                          </IconButton>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </CardContent>
      </Card>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Confirmar Exclusão</DialogTitle>
        <DialogContent>
          <Typography>
            Tem certeza que deseja deletar o arquivo "{fileToDelete?.name}"?
            Esta ação não pode ser desfeita.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancelar</Button>
          <Button onClick={handleDeleteConfirm} color="error" variant="contained">
            Deletar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default FileManager; 