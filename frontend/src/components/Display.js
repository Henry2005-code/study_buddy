// src/components/Display.js
import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import FlashcardDisplay from './FlashcardsDisplay';
import QuizDisplay from './QuizzesDisplay';
import { Box, Button, Typography, Grid } from '@mui/material';

const Display = () => {
  const location = useLocation();
  const generatedContent = location.state?.generatedContent || [];
  const contentType = location.state?.contentType || '';

  const totalItems = generatedContent.length;
  const [currentIndex, setCurrentIndex] = useState(0);

  const handlePrevious = () => {
    setCurrentIndex((prev) => (prev > 0 ? prev - 1 : prev));
  };

  const handleNext = () => {
    setCurrentIndex((prev) => (prev < totalItems - 1 ? prev + 1 : prev));
  };

  if (!totalItems) {
    return (
      <Box textAlign="center" mt={5}>
        <Typography variant="h4" gutterBottom>
          Error
        </Typography>
        <Typography variant="body1">
          No content to display. Please generate content first.
        </Typography>
      </Box>
    );
  }

  return (
    <Box textAlign="center" mt={5}>
      <Typography variant="h4" gutterBottom>
        Your Generated Content
      </Typography>
      <Grid container spacing={4} justifyContent="center">
        {contentType === 'flashcards' && (
          <Grid item xs={12} sm={8} md={6}>
            <FlashcardDisplay flashcard={generatedContent[currentIndex]} />
          </Grid>
        )}
        {contentType === 'quizzes' && (
          <Grid item xs={12} sm={8} md={6}>
            <QuizDisplay quiz={generatedContent[currentIndex]} />
          </Grid>
        )}
      </Grid>
      <Box mt={4} display="flex" justifyContent="center" alignItems="center">
        <Button
          variant="contained"
          color="primary"
          onClick={handlePrevious}
          disabled={currentIndex === 0}
          sx={{ mr: 2 }}
        >
          Previous
        </Button>
        <Typography variant="body1">
          {currentIndex + 1} / {totalItems}
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={handleNext}
          disabled={currentIndex === totalItems - 1}
          sx={{ ml: 2 }}
        >
          Next
        </Button>
      </Box>
      <Box mt={2}>
        <Button variant="outlined" color="secondary" href="/upload">
          Upload Another Document
        </Button>
      </Box>
    </Box>
  );
};

export default Display;
