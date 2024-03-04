import React from "react";
import {
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Button,
} from "@mui/material";

const DeviceTable = ({ devices, handleAddDevice }) => {
  return (
    <div>
      <Table
        style={{ width: "50%", margin: "0 40px", border: "1px solid black" }}
      >
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>Name</TableCell>
            <TableCell>Type</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {devices?.length > 0 &&
            devices.map((device) => (
              <TableRow key={device.id}>
                <TableCell>{device.id}</TableCell>
                <TableCell>{device.name}</TableCell>
                <TableCell>{device.type}</TableCell>
              </TableRow>
            ))}
        </TableBody>
      </Table>
      <Button onClick={handleAddDevice} variant="contained">
        Add Device
      </Button>
    </div>
  );
};

export default DeviceTable;
