import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Container,
} from '@mui/material';
import {
  Code,
  CompareArrows,
  Assessment,
  History,
} from '@mui/icons-material';

const HomePage = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <Code sx={{ fontSize: 40 }} />,
      title: 'Multi-Language Support',
      description: 'Supports Python, JavaScript, Java, C++, C#, and more',
    },
    {
      icon: <CompareArrows sx={{ fontSize: 40 }} />,
      title: 'AI-Powered Analysis',
      description: 'Uses advanced NLP and semantic analysis for accurate detection',
    },
    {
      icon: <Assessment sx={{ fontSize: 40 }} />,
      title: 'Detailed Reports',
      description: 'Get comprehensive similarity reports with explanations',
    },
    {
      icon: <History sx={{ fontSize: 40 }} />,
      title: 'Comparison History',
      description: 'Track and review your previous comparisons',
    },
  ];

  return (
    <Container maxWidth="lg">
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h2" component="h1" gutterBottom>
          AI-Powered Code Plagiarism Detector
        </Typography>
        <Typography variant="h5" component="h2" color="text.secondary" paragraph>
          Detect code plagiarism with advanced semantic analysis using AI and machine learning
        </Typography>
        <Box sx={{ mt: 4 }}>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/compare')}
            sx={{ mr: 2 }}
          >
            Start Comparison
          </Button>
          <Button
            variant="outlined"
            size="large"
            onClick={() => navigate('/history')}
          >
            View History
          </Button>
        </Box>
      </Box>

      <Grid container spacing={4}>
        {features.map((feature, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                textAlign: 'center',
                p: 2,
              }}
            >
              <CardContent>
                <Box sx={{ color: 'primary.main', mb: 2 }}>
                  {feature.icon}
                </Box>
                <Typography variant="h6" component="h3" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ mt: 6, textAlign: 'center' }}>
        <Typography variant="h4" component="h2" gutterBottom>
          How It Works
        </Typography>
        <Grid container spacing={3} sx={{ mt: 2 }}>
          <Grid item xs={12} md={4}>
            <Typography variant="h6" gutterBottom>
              1. Upload or Paste Code
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Upload code files or paste code snippets you want to compare
            </Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="h6" gutterBottom>
              2. AI Analysis
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Our AI analyzes the semantic structure and patterns in your code
            </Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="h6" gutterBottom>
              3. Get Results
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Receive detailed similarity scores and explanations
            </Typography>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default HomePage;