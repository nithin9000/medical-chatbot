import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const HospitalList = ({ location }) => {
  const [hospitals, setHospitals] = useState([]);
  const navigate = useNavigate(); // ✅ Correct hook

  useEffect(() => {
    if (location) {
      // Sample API call using location
      fetch(`https://api.example.com/hospitals?lat=${location.lat}&lon=${location.lon}`)
        .then((res) => res.json())
        .then((data) => setHospitals(data))
        .catch((err) => console.error(err));
    }
  }, [location]);

  const handleClick = (id) => {
    navigate(`/hospital/${id}`); // ✅ Correct usage
  };

  return (
    <div>
      <h2>Nearby Hospitals</h2>
      <ul>
        {hospitals.map((hosp) => (
          <li key={hosp.id} onClick={() => handleClick(hosp.id)}>
            {hosp.name}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default HospitalList;
