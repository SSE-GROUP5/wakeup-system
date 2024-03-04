import Button from '@mui/material/Button';

const SignalButtons = ({setOpenModal, setSelectedRow}) => {

  const handleAddSignle = () => {
    setSelectedRow(null);
    setOpenModal(true);
  }

  const handleEditSignal = () => {
    setOpenModal(true);
  }



  return (
    <div style={{marginTop: 20}}>
      <Button sx={{marginRight: 10}} variant="contained" color="primary" onClick={handleAddSignle}>Add Signal</Button>
      <Button variant="contained" color="primary" onClick={handleEditSignal}>Edit Signal</Button>
    </div>
  );
};

export default SignalButtons;