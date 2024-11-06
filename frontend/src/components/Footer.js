// src/components/Footer.js
import React from 'react';
import { Box, Typography } from '@mui/material';

const Footer = () => {
  return (
    <Box sx={{ bgcolor: 'primary.main', color: 'white', py: 2, mt: 'auto' }}>
      <Typography variant="body2" align="center">
        &copy; 2024 AI Learning Tool
      </Typography>
    </Box>
  );
};

export default Footer;
