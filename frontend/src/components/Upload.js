// src/components/Upload.js
import React, { useState } from 'react';
import axios from 'axios';

import {
  Typography,
  Button,
  Box,
  Input,
  LinearProgress,
  Snackbar,
  Alert,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Upload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = () => {
    if (!selectedFile) {
      setErrorMsg('Please select a file first.');
      setOpenSnackbar(true);
      return;
    }
    setUploading(true);
    const formData = new FormData();
    formData.append('document', selectedFile);

    axios
      .post('/api/upload', formData)
      .then((response) => {
        console.log('Upload response:', response.data);
        const userDataId = response.data.user_data_id;
        navigate('/generate', { state: { userDataId } });
      })
      .catch((error) => {
        console.error('Error uploading file:', error);
        setErrorMsg('An error occurred while uploading the file.');
        setOpenSnackbar(true);
      })
      .finally(() => {
        setUploading(false);
      });
  };

  return (
    <Box textAlign="center" mt={5}>
      <Typography variant="h4" gutterBottom>
        Upload Your Document
      </Typography>
      <Input
        type="file"
        onChange={handleFileChange}
        inputProps={{ accept: '.pdf,.txt,.docx,image/*' }}
      />
      <Typography variant="body2" color="textSecondary">
        Supported file types: .pdf, .txt, .docx, images
      </Typography>
      <Box mt={2}>
        <Button
          variant="contained"
          color="primary"
          onClick={handleUpload}
          disabled={uploading}
        >
          {uploading ? 'Uploading...' : 'Upload'}
        </Button>
      </Box>
      {uploading && <LinearProgress sx={{ mt: 2 }} />}
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

export default Upload;
