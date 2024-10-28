// src/components/FlashcardsDisplay.js
import React, { useState } from 'react';
import { Card, CardContent, Typography, Grid } from '@mui/material';
import { styled } from '@mui/system';

const FlipCard = styled('div')(({ flipped }) => ({
  perspective: '1000px',
  cursor: 'pointer',
  '& .inner': {
    position: 'relative',
    width: '100%',
    height: '200px',
    textAlign: 'center',
    transition: 'transform 0.6s',
    transformStyle: 'preserve-3d',
    transform: flipped ? 'rotateY(180deg)' : 'none',
  },
  '& .front, & .back': {
    position: 'absolute',
    width: '100%',
    height: '100%',
    backfaceVisibility: 'hidden',
    top: 0,
    left: 0,
  },
  '& .back': {
    transform: 'rotateY(180deg)',
  },
}));

const FlashcardsDisplay = ({ flashcards }) => {
  const [flippedCards, setFlippedCards] = useState({});

  const handleFlip = (index) => {
    setFlippedCards((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  return (
    <Grid container spacing={2}>
      {flashcards.map((card, index) => (
        <Grid item xs={12} sm={6} md={4} key={index}>
          <FlipCard
            onClick={() => handleFlip(index)}
            flipped={flippedCards[index]}
          >
            <div className="inner">
              <Card className="front">
                <CardContent>
                  <Typography variant="h5">{card.front}</Typography>
                </CardContent>
              </Card>
              <Card className="back">
                <CardContent>
                  <Typography variant="h6">{card.back}</Typography>
                </CardContent>
              </Card>
            </div>
          </FlipCard>
        </Grid>
      ))}
    </Grid>
  );
};

export default FlashcardsDisplay;
