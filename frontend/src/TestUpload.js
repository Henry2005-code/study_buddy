// src/TestUpload.js
import React, { useState } from 'react';
import axios from 'axios';

const TestUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [userDataId, setUserDataId] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = () => {
    if (!selectedFile) {
      alert('Please select a file first.');
      return;
    }
    const formData = new FormData();
    formData.append('document', selectedFile);

    axios.post('/api/upload', formData)
      .then(response => {
        console.log('Upload response:', response.data);
        setUserDataId(response.data.user_data_id);
      })
      .catch(error => {
        console.error('Error uploading file:', error);
      });
  };

  return (
    <div>
      <h1>Test File Upload</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      {userDataId && <p>User Data ID: {userDataId}</p>}
    </div>
  );
};

export default TestUpload;
