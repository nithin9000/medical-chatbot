import React, { useEffect, useState } from 'react';

const FindHospital = ({ location }) => {
  const [hospitals, setHospitals] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    if (location && location.lat && location.lon) {
      // Example API call (replace this with your actual hospital API)
      const fetchHospitals = async () => {
        try {
          // Replace with your actual API to find hospitals near the coordinates
          const response = await fetch(`https://api.example.com/hospitals?lat=${location.lat}&lon=${location.lon}`);
          const data = await response.json();
          if (data && data.length > 0) {
            setHospitals(data); // Update hospitals based on location
          } else {
            setError('No hospitals found in this location');
          }
        } catch (err) {
          setError('Error fetching hospitals');
          console.error(err);
        }
      };

      fetchHospitals();
    }
  }, [location]);

  return (
    <div>
      <h2>Hospitals near {location?.city}</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul>
        {hospitals.length > 0 ? (
          hospitals.map((hospital, index) => (
            <li key={index}>{hospital.name} - {hospital.address}</li>
          ))
        ) : (
          <li>No hospitals found for this location.</li>
        )}
      </ul>
    </div>
  );
};

export default FindHospital;
