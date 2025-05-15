import React, { useState } from 'react';

const LocationInput = ({ setLocation }) => {
  const [inputLocation, setInputLocation] = useState('');

  const handleLocationChange = (event) => {
    setInputLocation(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (inputLocation) {
      setLocation(inputLocation); // Updates the location state in App.js
    }
  };

  return (
    <div>
      <input
        type="text"
        value={inputLocation}
        onChange={handleLocationChange}
        placeholder="Enter your location"
      />
      <button onClick={handleSubmit}>Set Location</button>
    </div>
  );
};

export default LocationInput;
