import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Sidebar from './components/Sidebar';  
import Login from "./components/Login";
import Profile from "./components/Profile";
import DocumentsUploaded from "./components/DocumentsUploaded";
import FindHospital from "./components/FindHospital";
import CheckDoctorAvailability from "./components/CheckDoctorAvailability";
import AppointmentForm from "./components/AppointmentForm";
import LocationInput from "./components/LocationInput";  
import Footer from "./components/Footer";  
import './App.css';

const App = () => {
  const [location, setLocation] = useState(null);
  const [isDarkMode, setIsDarkMode] = useState(false);  // State for Dark Mode

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <Router>
      <div className={`App ${isDarkMode ? "dark" : "light"}`}>
        <Sidebar />  
        <div className="content">
          <h1>Medical Chatbot for Travelers</h1>
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/profile" element={<Profile setLocation={setLocation} />} />
            <Route path="/documents" element={<DocumentsUploaded />} />
            <Route path="/find-hospital" element={<FindHospital location={location} />} />
            <Route path="/check-availability" element={<CheckDoctorAvailability />} />
            <Route path="/appointments" element={<AppointmentForm />} />
          </Routes>
        </div>
        
        {/* Dark Mode Toggle */}
        <div className="theme-toggle">
          <label className="switch">
            <input type="checkbox" checked={isDarkMode} onChange={toggleTheme} />
            <span className="slider"></span>
          </label>
        </div>

        <Footer />  
      </div>
    </Router>
  );
};

export default App;
