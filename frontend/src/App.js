// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CssBaseline, Container } from '@mui/material';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './components/Home';
import Upload from './components/Upload';
import Generate from './components/Generate';
import Display from './components/Display';

function App() {
  return (
    <Router>
      <CssBaseline />
      <Navbar />
      <Container maxWidth="md" style={{ marginTop: '2rem', marginBottom: '2rem' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/generate" element={<Generate />} />
          <Route path="/display" element={<Display />} />
        </Routes>
      </Container>
      <Footer />
    </Router>
  );
}

export default App;
