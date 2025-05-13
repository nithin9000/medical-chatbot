import React, { useState } from "react";
import { FaSearch } from "react-icons/fa"; // FontAwesome Search Icon
import '../App.css';  // Import the App.css file

const Profile = ({ setLocation }) => {
  const [searchQuery, setSearchQuery] = useState("");

  // Function to handle location search
  const handleSearch = () => {
    console.log("Searching for: ", searchQuery);
    setLocation(searchQuery);  // Update the parent component's state with the searched location
  };

  // Function to detect the user's current location
  const handleDetectLocation = () => {
    console.log("Detecting current location...");
    // You can use Geolocation API or any external API to detect location
    // Here, I'm using a mock location for simplicity
    const detectedLocation = "New York, USA"; // Example location
    setLocation(detectedLocation);  // Set the detected location
  };

  return (
    <div className="profile-location-search">
      {/* Search Input with Search Icon */}
      <div className="profile-location-input">
        <input
          type="text"
          placeholder="Search for a location"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)} // Update the search query
        />
        <FaSearch className="search-icon" onClick={handleSearch} />
      </div>

      {/* Detect My Location Button */}
      <button onClick={handleDetectLocation} className="detect-location-button">
        Detect My Location
      </button>
    </div>
  );
};

export default Profile;
