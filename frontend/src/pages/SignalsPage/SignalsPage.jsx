import { useEffect, useState } from "react";
import { apiService } from "../../api";
import { Paper } from "@mui/material";
import CircularProgress from "@mui/material/CircularProgress";
import SignalsTable from "./SignalsTable";
import SignalButtons from "./SignalButtons";
import AddSignalModal from "./AddSignalModal";

export default function SignalsPage() {
  const [signals, setSignals] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [targets, setTargets] = useState([]);
  const [triggers, setTriggers] = useState([]);
  const [openModal, setOpenModal] = useState(false);
  const [selectedRow, setSelectedRow] = useState(null);

  const getTargets = async () => {
    try {
      const response = await apiService.targets.getTargets();
      setTargets(response);
    } catch (error) {
      console.error(error);
    }
  };

  const getTriggers = async () => {
    try {
      const response = await apiService.triggers.getTriggers();
      setTriggers(response);
    } catch (error) {
      console.error(error);
    }
  };

  const getSignals = async () => {
    try {
      setLoading(true);
      const response = await apiService.signals.getSignals();
      setSignals(response);
    } catch (error) {
      setError(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    console.log(selectedRow);
  }, [selectedRow]);

  useEffect(() => {
    getSignals();
    getTargets();
    getTriggers();
  }, [openModal]);

  if (loading) {
    return <CircularProgress />;
  }

  if (signals.length === 0) {
    return <Paper>No signals found</Paper>;
  }

  return (
    <div>
      <SignalsTable signals={signals} setSelectedRow={setSelectedRow} selectedRow={selectedRow} />
      <SignalButtons setOpenModal={setOpenModal} setSelectedRow={setSelectedRow} />
      {openModal && (
        <AddSignalModal
          triggers={triggers}
          targets={targets}
          selectedRow={selectedRow}
          openModal={openModal}
          setOpenModal={setOpenModal}
        />
      )}
    </div>
  );
}
