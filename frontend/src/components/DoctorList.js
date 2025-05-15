import React, { useState, useEffect } from "react";
import axios from "axios";

const DoctorList = ({ match }) => {
  const { hospitalId } = match.params;
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    axios
      .get(`/api/doctors?hospitalId=${hospitalId}`)
      .then((response) => {
        setDoctors(response.data);
      })
      .catch((error) => {
        console.error("Error fetching doctor data", error);
      })
      .finally(() => setLoading(false));
  }, [hospitalId]);

  if (loading) return <p>Loading doctors...</p>;

  return (
    <div>
      <h2>Doctors in the hospital</h2>
      {doctors.length > 0 ? (
        <ul>
          {doctors.map((doctor) => (
            <li key={doctor.id}>
              <h3>{doctor.name}</h3>
              <p>{doctor.specialty}</p>
              <p>Available: {doctor.availableFrom} - {doctor.availableTo}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No doctors found in this hospital.</p>
      )}
    </div>
  );
};

export default DoctorList;
