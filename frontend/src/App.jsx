import React from 'react';
import { Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';  
import HeroSection from './components/HeroSection';
import Work from './components/Work';
import Learn from './components/Learn';
import Profile from './components/Profile';

const App = () => {
  return (
    <div>
      <NavBar /> 
      <Routes>
        <Route path="/" element={<HeroSection />} />
        <Route path="/workout" element={<Work />} />
        <Route path="/learn" element={<Learn />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </div>
  );
};

export default App;
