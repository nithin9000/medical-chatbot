import React, { useState } from 'react';

const AppointmentForm = () => {
  const [hospital, setHospital] = useState('');
  const [doctor, setDoctor] = useState('');
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [appointments, setAppointments] = useState([]);

  const handleSubmit = (e) => {
    e.preventDefault();

    // Create a new appointment object
    const newAppointment = {
      hospital,
      doctor,
      date,
      time,
    };

    // Add new appointment to the state
    setAppointments([...appointments, newAppointment]);

    // Clear the form fields
    setHospital('');
    setDoctor('');
    setDate('');
    setTime('');
  };

  return (
    <div className="appointment-form-container">
      <h2>Book an Appointment</h2>
      
      <form onSubmit={handleSubmit}>
        <div>
          <label>Hospital:</label>
          <input
            type="text"
            value={hospital}
            onChange={(e) => setHospital(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Doctor:</label>
          <input
            type="text"
            value={doctor}
            onChange={(e) => setDoctor(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Date:</label>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Time:</label>
          <input
            type="time"
            value={time}
            onChange={(e) => setTime(e.target.value)}
            required
          />
        </div>

        <button type="submit">Book Appointment</button>
      </form>

      <h3>Your Appointments</h3>
      {appointments.length === 0 ? (
        <p>No appointments booked yet.</p>
      ) : (
        <ul>
          {appointments.map((appointment, index) => (
            <li key={index}>
              <strong>Hospital:</strong> {appointment.hospital}, 
              <strong>Doctor:</strong> {appointment.doctor}, 
              <strong>Date:</strong> {appointment.date}, 
              <strong>Time:</strong> {appointment.time}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AppointmentForm;
