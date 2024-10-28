// src/components/Home.js
import React from 'react';
import { Typography, Button, Stack } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Home = () => {
  return (
    <Stack spacing={4} alignItems="center" mt={5}>
      <Typography variant="h3" component="h1" gutterBottom>
        Welcome to the AI Learning Tool
      </Typography>
      <Typography variant="h5" component="p" align="center">
        Generate personalized study aids like flashcards and quizzes from your documents.
      </Typography>
      <Button variant="contained" size="large" component={RouterLink} to="/upload">
        Get Started
      </Button>
    </Stack>
  );
};

export default Home;
