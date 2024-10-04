// src/TestGenerate.js
import React, { useState } from 'react';
import axios from 'axios';

const TestGenerate = () => {
  const [userDataId, setUserDataId] = useState('');
  const [contentType, setContentType] = useState('flashcards');
  const [numItems, setNumItems] = useState(5);
  const [generatedContent, setGeneratedContent] = useState('');

  const handleGenerate = () => {
    axios.post('/api/generate', {
      user_data_id: parseInt(userDataId),
      content_type: contentType,
      num_items: parseInt(numItems),
    })
      .then(response => {
        console.log('Generate response:', response.data);
        setGeneratedContent(response.data.generated_content);
      })
      .catch(error => {
        console.error('Error generating content:', error);
      });
  };

  return (
    <div>
      <h1>Test Content Generation</h1>
      <input
        type="number"
        placeholder="User Data ID"
        value={userDataId}
        onChange={(e) => setUserDataId(e.target.value)}
      />
      <select value={contentType} onChange={(e) => setContentType(e.target.value)}>
        <option value="flashcards">Flashcards</option>
        <option value="quizzes">Quizzes</option>
      </select>
      <input
        type="number"
        placeholder="Number of Items"
        value={numItems}
        onChange={(e) => setNumItems(e.target.value)}
      />
      <button onClick={handleGenerate}>Generate</button>
      {generatedContent && (
        <div>
          <h2>Generated Content:</h2>
          <pre>{generatedContent}</pre>
        </div>
      )}
    </div>
  );
};

export default TestGenerate;
