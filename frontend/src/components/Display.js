// src/components/Display.js
import React from 'react';
import { useLocation } from 'react-router-dom';
import FlashcardsDisplay from './FlashcardsDisplay';
import QuizzesDisplay from './QuizzesDisplay';

const Display = () => {
  const location = useLocation();
  const generatedContent = location.state?.generatedContent || [];
  const contentType = location.state?.contentType || '';

  if (!generatedContent.length) {
    return (
      <div>
        <h2>Error</h2>
        <p>No content to display. Please generate content first.</p>
      </div>
    );
  }

  return (
    <div>
      {contentType === 'flashcards' && (
        <FlashcardsDisplay flashcards={generatedContent} />
      )}
      {contentType === 'quizzes' && (
        <QuizzesDisplay quizzes={generatedContent} />
      )}
    </div>
  );
};

export default Display;
