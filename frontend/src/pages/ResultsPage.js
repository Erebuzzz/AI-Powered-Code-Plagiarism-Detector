import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  Grid,
  LinearProgress,
  Chip,
  Card,
  CardContent,
  Alert,
  CircularProgress,
} from '@mui/material';
import Editor from '@monaco-editor/react';
import { apiService } from '../services/api';

const ResultsPage = () => {
  const { id } = useParams();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const data = await apiService.getReport(id);
        setReport(data);
      } catch (err) {
        setError('Error fetching report: ' + err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchReport();
  }, [id]);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        {error}
      </Alert>
    );
  }

  const getSimilarityColor = (score) => {
    if (score >= 0.7) return 'error';
    if (score >= 0.4) return 'warning';
    return 'success';
  };

  const getSimilarityLabel = (score) => {
    if (score >= 0.7) return 'High Similarity';
    if (score >= 0.4) return 'Medium Similarity';
    return 'Low Similarity';
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Comparison Results
      </Typography>

      {report && (
        <>
          {/* Summary Card */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Grid container spacing={3} alignItems="center">
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  Similarity Score
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ width: '100%', mr: 1 }}>
                    <LinearProgress
                      variant="determinate"
                      value={report.similarity_score * 100}
                      color={getSimilarityColor(report.similarity_score)}
                      sx={{ height: 10, borderRadius: 5 }}
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {(report.similarity_score * 100).toFixed(1)}%
                  </Typography>
                </Box>
                <Chip
                  label={getSimilarityLabel(report.similarity_score)}
                  color={getSimilarityColor(report.similarity_score)}
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  Plagiarism Status
                </Typography>
                <Chip
                  label={report.is_plagiarized ? 'PLAGIARIZED' : 'ORIGINAL'}
                  color={report.is_plagiarized ? 'error' : 'success'}
                  size="large"
                />
              </Grid>
            </Grid>
          </Paper>

          {/* Analysis Details */}
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    File 1: {report.file1_name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Language: {report.language1}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Tokens: {report.analysis?.code1_tokens || 'N/A'}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    File 2: {report.file2_name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Language: {report.language2}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Tokens: {report.analysis?.code2_tokens || 'N/A'}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* AI Explanation */}
          {report.analysis?.explanation && (
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                AI Analysis
              </Typography>
              <Typography variant="body1">
                {report.analysis.explanation}
              </Typography>
            </Paper>
          )}

          {/* Detailed Scores */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Detailed Analysis
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={4}>
                <Typography variant="body2" color="text.secondary">
                  Semantic Similarity
                </Typography>
                <Typography variant="h6">
                  {(report.similarity_score * 100).toFixed(1)}%
                </Typography>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Typography variant="body2" color="text.secondary">
                  Lexical Similarity
                </Typography>
                <Typography variant="h6">
                  {((report.analysis?.lexical_similarity || 0) * 100).toFixed(1)}%
                </Typography>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Typography variant="body2" color="text.secondary">
                  Common Tokens
                </Typography>
                <Typography variant="h6">
                  {report.analysis?.common_tokens || 0}
                </Typography>
              </Grid>
            </Grid>
          </Paper>

          {/* Side-by-side Code Comparison */}
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Code Comparison
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle1" gutterBottom>
                  {report.file1_name}
                </Typography>
                <Box sx={{ border: 1, borderColor: 'grey.300', borderRadius: 1 }}>
                  <Editor
                    height="400px"
                    language={report.language1}
                    value={report.code1}
                    options={{
                      readOnly: true,
                      minimap: { enabled: false },
                      fontSize: 12,
                    }}
                    theme="vs-light"
                  />
                </Box>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle1" gutterBottom>
                  {report.file2_name}
                </Typography>
                <Box sx={{ border: 1, borderColor: 'grey.300', borderRadius: 1 }}>
                  <Editor
                    height="400px"
                    language={report.language2}
                    value={report.code2}
                    options={{
                      readOnly: true,
                      minimap: { enabled: false },
                      fontSize: 12,
                    }}
                    theme="vs-light"
                  />
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </>
      )}
    </Box>
  );
};

export default ResultsPage;