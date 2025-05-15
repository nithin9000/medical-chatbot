import React from "react";
import { Link } from "react-router-dom";
import "./Sidebar.css"; // Assuming you have a separate CSS file

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>Medical Chatbot</h2>
      </div>
      <div className="sidebar-links">
        <Link to="/profile" className="sidebar-link">
          Profile
        </Link>
        <Link to="/documents" className="sidebar-link">
          Uploaded Documents
        </Link>
        <Link to="/find-hospital" className="sidebar-link">
          Find Hospital
        </Link>
        <Link to="/doctor-availability" className="sidebar-link">
          Doctor Availability
        </Link>
        <Link to="/appointments" className="sidebar-link">
          Appointments
        </Link>
      </div>
    </div>
  );
};

export default Sidebar;
