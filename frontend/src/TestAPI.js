// src/TestAPI.js
import React, { useEffect } from 'react';
import axios from 'axios';

const TestAPI = () => {
  useEffect(() => {
    axios.get('/api/test')
      .then(response => {
        console.log('Response from backend:', response.data);
      })
      .catch(error => {
        console.error('Error fetching from backend:', error);
      });
  }, []);

  return (
    <div>
      <h1>Testing Backend Connectivity</h1>
      <p>Check the console for the backend response.</p>
    </div>
  );
};

export default TestAPI;
