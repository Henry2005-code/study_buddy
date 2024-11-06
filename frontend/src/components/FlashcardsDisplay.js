// src/components/FlashcardDisplay.js
import React, { useState } from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import { styled } from '@mui/system';

const StyledCard = styled(Card)(({ flipped }) => ({
  width: '100%',
  height: '200px',
  perspective: '1000px',
  cursor: 'pointer',
  position: 'relative',
}));

const InnerCard = styled('div')(({ flipped }) => ({
  position: 'absolute',
  width: '100%',
  height: '100%',
  textAlign: 'center',
  transition: 'transform 0.6s',
  transformStyle: 'preserve-3d',
  transform: flipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
}));

const CardFace = styled(CardContent)(({ front }) => ({
  position: 'absolute',
  width: '100%',
  height: '100%',
  backfaceVisibility: 'hidden',
  WebkitBackfaceVisibility: 'hidden',
  backgroundColor: front ? '#ffffff' : '#f0f0f0',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  padding: '16px',
  border: '1px solid #ddd',
  borderRadius: '8px',
}));

const FlashcardDisplay = ({ flashcard }) => {
  const [flipped, setFlipped] = useState(false);

  const handleFlip = () => {
    setFlipped((prev) => !prev);
  };

  return (
    <Box textAlign="center">
      <StyledCard onClick={handleFlip}>
        <InnerCard flipped={flipped}>
          {/* Front Face */}
          <CardFace front>
            <Typography variant="h5">{flashcard.front}</Typography>
          </CardFace>
          {/* Back Face */}
          <CardFace
            front={false}
            sx={{
              transform: 'rotateY(180deg)', // Rotate back face to correct orientation
            }}
          >
            <Typography variant="h6">{flashcard.back}</Typography>
          </CardFace>
        </InnerCard>
      </StyledCard>
      <Typography variant="caption" display="block" mt={1}>
        Click the card to {flipped ? 'hide' : 'show'} the answer.
      </Typography>
    </Box>
  );
};

export default FlashcardDisplay;
