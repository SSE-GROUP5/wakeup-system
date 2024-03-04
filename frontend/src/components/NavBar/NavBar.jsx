import React from 'react';
import { Button } from '@mui/material';
import './styles.css';

const NavBar = () => {

  const goToSignals = () => {
    window.location.href = '/signals';
  }

  const goToDevices = () => {
    window.location.href = '/devices';
  }


  return (
    <nav className="navbar">
      <Button sx={{marginRight: "10px"}} variant="contained" to="/signals" onClick={goToSignals}>Signals</Button>
      <Button variant="contained" to="/devices" onClick={goToDevices}>Devices</Button>
    </nav>
  );
};

export default NavBar;