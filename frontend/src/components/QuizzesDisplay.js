// src/components/QuizzesDisplay.js
import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Radio,
  RadioGroup,
  FormControlLabel,
  Button,
  Box,
  Alert,
} from '@mui/material';

const QuizzesDisplay = ({ quiz }) => {
  const [selectedOption, setSelectedOption] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);

  const handleChange = (event) => {
    setSelectedOption(event.target.value);
  };

  const handleSubmit = () => {
    if (!selectedOption) return;
    setIsCorrect(selectedOption === quiz.answer);
    setSubmitted(true);
  };

  return (
    <Box textAlign="center">
      <Card sx={{ minHeight: '200px' }}>
        <CardContent>
          <Typography variant="h6">{quiz.question}</Typography>
          <RadioGroup
            value={selectedOption}
            onChange={handleChange}
            sx={{ textAlign: 'left', mt: 2 }}
          >
            {quiz.options.map((option, index) => (
              <FormControlLabel
                key={index}
                value={option}
                control={<Radio />}
                label={option}
                disabled={submitted}
              />
            ))}
          </RadioGroup>
          {!submitted ? (
            <Button
              variant="contained"
              color="primary"
              onClick={handleSubmit}
              disabled={!selectedOption}
              sx={{ mt: 2 }}
            >
              Submit
            </Button>
          ) : (
            <Box mt={2}>
              {isCorrect ? (
                <Alert severity="success">Correct!</Alert>
              ) : (
                <Alert severity="error">
                  Incorrect. The correct answer is: {quiz.answer}
                </Alert>
              )}
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default QuizzesDisplay;
