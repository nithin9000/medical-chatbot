import React from 'react';
import { useParams } from 'react-router-dom';

const CheckDoctorAvailability = () => {
  const { hospitalId } = useParams();

  // Sample data (replace with an actual API call)
  const doctors = [
    { id: 1, name: 'Dr. Smith', availableFrom: '9:00 AM', availableTo: '5:00 PM' },
    { id: 2, name: 'Dr. Johnson', availableFrom: '10:00 AM', availableTo: '4:00 PM' },
  ];

  return (
    <div>
      <h2>Doctors Available at Hospital {hospitalId}</h2>
      <ul>
        {doctors.map(doctor => (
          <li key={doctor.id}>
            <p>{doctor.name}</p>
            <p>Available: {doctor.availableFrom} to {doctor.availableTo}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CheckDoctorAvailability;
