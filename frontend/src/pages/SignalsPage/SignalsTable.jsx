import {
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
} from "@mui/material";
import { maxHeight } from "@mui/system";

// eslint-disable-next-line react/prop-types
const SignalsTable = ({ signals, setSelectedRow, selectedRow }) => {
  
  const handleRowClick = (signal) => {
    setSelectedRow(signal);
  }


  return (
    <TableContainer component={Paper} sx={{maxHeight: 700, overflow: 'auto', overflowY: 'scroll'}}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>Target Action</TableCell>
            <TableCell>Target ID</TableCell>
            <TableCell>Trigger Action</TableCell>
            <TableCell>Trigger ID</TableCell>
            <TableCell>Trigger Name</TableCell>
            <TableCell>Trigger Num Actions</TableCell>
            <TableCell>User ID</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {signals.map((signal) => (
            <TableRow 
              onClick={() => handleRowClick(signal)}
              key={signal.id}
              sx={{ "&:last-child td, &:last-child th": { border: 0 } , backgroundColor: signal.id === selectedRow?.id ? "lightgray" : "white"}}
            >
              <TableCell>{signal.id}</TableCell>
              <TableCell>{signal.target_action}</TableCell>
              <TableCell>{signal.target_id}</TableCell>
              <TableCell>{signal.trigger_action}</TableCell>
              <TableCell>{signal.trigger_id}</TableCell>
              <TableCell>{signal.trigger_name}</TableCell>
              <TableCell>{signal.trigger_num_actions}</TableCell>
              <TableCell>{signal.user_id}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default SignalsTable;