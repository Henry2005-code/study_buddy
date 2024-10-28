// src/components/Generate.js
import React, { useState } from 'react';
import axios from 'axios';

import {
  Typography,
  Button,
  Box,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  LinearProgress,
  Snackbar,
  Alert,
} from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';

const Generate = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const userDataId = location.state?.userDataId || null;
  const [contentType, setContentType] = useState('flashcards');
  const [numItems, setNumItems] = useState(5);
  const [generating, setGenerating] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);

  if (!userDataId) {
    return (
      <Box textAlign="center" mt={5}>
        <Typography variant="h4" gutterBottom>
          Error
        </Typography>
        <Typography variant="body1">
          No user data found. Please upload a document first.
        </Typography>
      </Box>
    );
  }

  const handleGenerate = () => {
    setGenerating(true);
    axios
      .post('/api/generate', {
        user_data_id: userDataId,
        content_type: contentType,
        num_items: parseInt(numItems),
      })
      .then((response) => {
        console.log('Generate response:', response.data);
        const generatedContent = response.data.generated_content;
        navigate('/display', { state: { generatedContent, contentType } });
      })
      .catch((error) => {
        console.error('Error generating content:', error);
        setErrorMsg('An error occurred while generating content.');
        setOpenSnackbar(true);
      })
      .finally(() => {
        setGenerating(false);
      });
  };

  return (
    <Box textAlign="center" mt={5}>
      <Typography variant="h4" gutterBottom>
        Generate Your Study Aids
      </Typography>
      <FormControl sx={{ m: 1, minWidth: 240 }}>
        <InputLabel>Content Type</InputLabel>
        <Select
          value={contentType}
          onChange={(e) => setContentType(e.target.value)}
          label="Content Type"
        >
          <MenuItem value="flashcards">Flashcards</MenuItem>
          <MenuItem value="quizzes">Quizzes</MenuItem>
        </Select>
      </FormControl>
      <TextField
        label="Number of Items"
        type="number"
        value={numItems}
        onChange={(e) => setNumItems(e.target.value)}
        InputProps={{ inputProps: { min: 1, max: 20 } }}
        sx={{ m: 1, minWidth: 240 }}
      />
      <Box mt={2}>
        <Button
          variant="contained"
          color="primary"
          onClick={handleGenerate}
          disabled={generating}
        >
          {generating ? 'Generating...' : 'Generate'}
        </Button>
      </Box>
      {generating && <LinearProgress sx={{ mt: 2 }} />}
      <Snackbar
        open={openSnackbar}
        autoHideDuration={6000}
        onClose={() => setOpenSnackbar(false)}
      >
        <Alert severity="error" onClose={() => setOpenSnackbar(false)}>
          {errorMsg}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Generate;
