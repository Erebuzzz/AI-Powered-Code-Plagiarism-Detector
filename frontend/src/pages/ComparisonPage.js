import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Tab,
  Tabs,
  Alert,
  CircularProgress,
} from '@mui/material';
import { useDropzone } from 'react-dropzone';
import Editor from '@monaco-editor/react';
import { apiService } from '../services/api';

const SUPPORTED_LANGUAGES = [
  { value: 'python', label: 'Python' },
  { value: 'javascript', label: 'JavaScript' },
  { value: 'java', label: 'Java' },
  { value: 'cpp', label: 'C++' },
  { value: 'c', label: 'C' },
  { value: 'csharp', label: 'C#' },
];

const ComparisonPage = () => {
  const navigate = useNavigate();
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Code input states
  const [code1, setCode1] = useState('');
  const [code2, setCode2] = useState('');
  const [language1, setLanguage1] = useState('python');
  const [language2, setLanguage2] = useState('python');
  
  // File upload states
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);

  const onDrop1 = (acceptedFiles) => {
    setFile1(acceptedFiles[0]);
  };

  const onDrop2 = (acceptedFiles) => {
    setFile2(acceptedFiles[0]);
  };

  const { getRootProps: getRootProps1, getInputProps: getInputProps1 } = useDropzone({
    onDrop: onDrop1,
    accept: {
      'text/plain': ['.txt', '.py', '.js', '.java', '.cpp', '.c', '.cs'],
    },
    maxFiles: 1,
  });

  const { getRootProps: getRootProps2, getInputProps: getInputProps2 } = useDropzone({
    onDrop: onDrop2,
    accept: {
      'text/plain': ['.txt', '.py', '.js', '.java', '.cpp', '.c', '.cs'],
    },
    maxFiles: 1,
  });

  const handleCompareCode = async () => {
    if (!code1.trim() || !code2.trim()) {
      setError('Please enter code in both editors');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await apiService.compareCode(code1, code2, language1, language2);
      navigate(`/results/${result.comparison_id}`);
    } catch (err) {
      setError('Error comparing code: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadFiles = async () => {
    if (!file1 || !file2) {
      setError('Please upload both files');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await apiService.uploadFiles(file1, file2, language1, language2);
      navigate(`/results/${result.comparison_id}`);
    } catch (err) {
      setError('Error uploading files: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Code Comparison
      </Typography>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
          <Tab label="Paste Code" />
          <Tab label="Upload Files" />
        </Tabs>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}

        {tabValue === 0 && (
          <Box sx={{ mt: 3 }}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  Code 1
                </Typography>
                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel>Language</InputLabel>
                  <Select
                    value={language1}
                    onChange={(e) => setLanguage1(e.target.value)}
                  >
                    {SUPPORTED_LANGUAGES.map((lang) => (
                      <MenuItem key={lang.value} value={lang.value}>
                        {lang.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <Box sx={{ border: 1, borderColor: 'grey.300', borderRadius: 1 }}>
                  <Editor
                    height="400px"
                    language={language1}
                    value={code1}
                    onChange={(value) => setCode1(value || '')}
                    theme="vs-dark"
                    options={{
                      minimap: { enabled: false },
                      fontSize: 14,
                    }}
                  />
                </Box>
              </Grid>

              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  Code 2
                </Typography>
                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel>Language</InputLabel>
                  <Select
                    value={language2}
                    onChange={(e) => setLanguage2(e.target.value)}
                  >
                    {SUPPORTED_LANGUAGES.map((lang) => (
                      <MenuItem key={lang.value} value={lang.value}>
                        {lang.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <Box sx={{ border: 1, borderColor: 'grey.300', borderRadius: 1 }}>
                  <Editor
                    height="400px"
                    language={language2}
                    value={code2}
                    onChange={(value) => setCode2(value || '')}
                    theme="vs-dark"
                    options={{
                      minimap: { enabled: false },
                      fontSize: 14,
                    }}
                  />
                </Box>
              </Grid>
            </Grid>

            <Box sx={{ mt: 3, textAlign: 'center' }}>
              <Button
                variant="contained"
                size="large"
                onClick={handleCompareCode}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Compare Code'}
              </Button>
            </Box>
          </Box>
        )}

        {tabValue === 1 && (
          <Box sx={{ mt: 3 }}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  File 1
                </Typography>
                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel>Language</InputLabel>
                  <Select
                    value={language1}
                    onChange={(e) => setLanguage1(e.target.value)}
                  >
                    {SUPPORTED_LANGUAGES.map((lang) => (
                      <MenuItem key={lang.value} value={lang.value}>
                        {lang.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <Paper
                  {...getRootProps1()}
                  sx={{
                    p: 3,
                    textAlign: 'center',
                    cursor: 'pointer',
                    border: '2px dashed',
                    borderColor: file1 ? 'success.main' : 'grey.300',
                    bgcolor: file1 ? 'success.light' : 'grey.50',
                  }}
                >
                  <input {...getInputProps1()} />
                  {file1 ? (
                    <Typography>Selected: {file1.name}</Typography>
                  ) : (
                    <Typography>
                      Drag & drop a code file here, or click to select
                    </Typography>
                  )}
                </Paper>
              </Grid>

              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  File 2
                </Typography>
                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel>Language</InputLabel>
                  <Select
                    value={language2}
                    onChange={(e) => setLanguage2(e.target.value)}
                  >
                    {SUPPORTED_LANGUAGES.map((lang) => (
                      <MenuItem key={lang.value} value={lang.value}>
                        {lang.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <Paper
                  {...getRootProps2()}
                  sx={{
                    p: 3,
                    textAlign: 'center',
                    cursor: 'pointer',
                    border: '2px dashed',
                    borderColor: file2 ? 'success.main' : 'grey.300',
                    bgcolor: file2 ? 'success.light' : 'grey.50',
                  }}
                >
                  <input {...getInputProps2()} />
                  {file2 ? (
                    <Typography>Selected: {file2.name}</Typography>
                  ) : (
                    <Typography>
                      Drag & drop a code file here, or click to select
                    </Typography>
                  )}
                </Paper>
              </Grid>
            </Grid>

            <Box sx={{ mt: 3, textAlign: 'center' }}>
              <Button
                variant="contained"
                size="large"
                onClick={handleUploadFiles}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Upload and Compare'}
              </Button>
            </Box>
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default ComparisonPage;