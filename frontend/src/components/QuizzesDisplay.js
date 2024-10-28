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
} from '@mui/material';

const QuizzesDisplay = ({ quizzes }) => {
  const [userAnswers, setUserAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);

  const handleAnswerChange = (questionIndex, option) => {
    setUserAnswers((prev) => ({
      ...prev,
      [questionIndex]: option,
    }));
  };

  const handleSubmit = () => {
    setShowResults(true);
  };

  const getScore = () => {
    let score = 0;
    quizzes.forEach((quiz, index) => {
      if (userAnswers[index] === quiz.answer) {
        score += 1;
      }
    });
    return score;
  };

  return (
    <Box>
      {quizzes.map((quiz, index) => (
        <Card key={index} sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="h6">
              {index + 1}. {quiz.question}
            </Typography>
            <RadioGroup
              value={userAnswers[index] || ''}
              onChange={(e) => handleAnswerChange(index, e.target.value)}
            >
              {quiz.options.map((option, optIndex) => (
                <FormControlLabel
                  key={optIndex}
                  value={option}
                  control={<Radio />}
                  label={option}
                  disabled={showResults}
                />
              ))}
            </RadioGroup>
            {showResults && (
              <Typography
                variant="body2"
                color={
                  userAnswers[index] === quiz.answer ? 'success.main' : 'error.main'
                }
              >
                {userAnswers[index] === quiz.answer
                  ? 'Correct!'
                  : `Incorrect. Correct answer: ${quiz.answer}`}
              </Typography>
            )}
          </CardContent>
        </Card>
      ))}
      {!showResults && (
        <Button variant="contained" onClick={handleSubmit}>
          Submit Answers
        </Button>
      )}
      {showResults && (
        <Typography variant="h5" mt={2}>
          Your Score: {getScore()} / {quizzes.length}
        </Typography>
      )}
    </Box>
  );
};

export default QuizzesDisplay;
