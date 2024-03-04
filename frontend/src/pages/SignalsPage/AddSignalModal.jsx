import React, { useEffect, useState } from "react";
import { Button, Modal } from "@mui/material";
import { apiService } from "../../api";
import {
  FormControl,
  InputLabel,
  NativeSelect,
  TextField,
} from "@mui/material";
import "./styles.css";

const AddSignalModal = ({ triggers, targets, selectedRow, setOpenModal }) => {
  const [targetActions, setTargetActions] = useState([]);

  const [form, setForm] = useState(() =>
    selectedRow
      ? {
          target_device_id: selectedRow.target_id,
          target_action: selectedRow.target_action,
          trigger_action: selectedRow.trigger_action,
          trigger_id: selectedRow.trigger_id,
          trigger_num_actions: selectedRow.trigger_num_actions,

        }
      : {
          target_device_id: targets[0]?.matter_id || "",
          target_action: "",
          trigger_action: "",
          trigger_id: triggers[0]?.id || "",
          trigger_num_actions: "",
        }
  );

  const handleClose = () => {
    setOpenModal(false);
  };

  const handleSignalChange = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const handleAddSignal = async () => {
    // Add your logic to handle adding the signal here
    try {
      const trigger = triggers.find(
        (trigger) => trigger.id === form.trigger_id
      );
      const newSignal = {
        ...form,
        trigger_action: trigger.type,
      };
      await apiService.signals.addSignal(newSignal);
      handleClose();
    } catch (error) {
      console.error(error);
    }
  };

  const getTargetActionss = (targetId) => {
    if (targets.length === 0) return;
    const target = targets.find((target) => target.matter_id === targetId);

    if (!target) return;
    setTargetActions(target.possible_actions);
    setForm({ ...form, target_action: target.possible_actions[0].action });
  };

  useEffect(() => {
    if (!form.target_device_id) return;

    getTargetActionss(form.target_device_id);
  }, [form.target_device_id]);

  return (
    <Modal open={open} onClose={handleClose} className="modalContainer">
      <div className="modalContent">
        <h2>Add Signal</h2>

        <InputLabel variant="standard" htmlFor="uncontrolled-native">
          Trigger
        </InputLabel>
        <FormControl fullWidth className="formControl">
          <NativeSelect
            className="nativeSelect"
            value={form.trigger_id}
            onChange={(event) => handleSignalChange(event)}
            inputProps={{
              name: "trigger_id",
              id: "uncontrolled-native",
            }}
          >
            {triggers?.length > 0 &&
              triggers.map((trigger) => (
                <option key={trigger.id} value={trigger.id}>
                  {trigger.name}
                </option>
              ))}
          </NativeSelect>
        </FormControl>

        {/* Add triger action which is an input field of max 3 characters */}
        <InputLabel variant="standard" htmlFor="uncontrolled-native">
          Trigger Number of Times (or letter for Morse)
        </InputLabel>
        <TextField
          className="nativeSelect"
          name="trigger_num_actions"
          value={form.trigger_num_actions}
          InputProps={{ inputProps: { maxLength: 3 } }}
          onChange={(event) => handleSignalChange(event)}
        />

        <InputLabel variant="standard" htmlFor="uncontrolled-native">
          Target
        </InputLabel>
        <FormControl fullWidth className="formControl">
          <NativeSelect
            className="nativeSelect"
            value={form.target_device_id}
            onChange={(event) => handleSignalChange(event)}
            inputProps={{
              name: "target_device_id",
              id: "uncontrolled-native",
            }}
          >
            {targets?.length > 0 &&
              targets.map((target) => (
                <option key={target.id} value={target.id}>
                  {target.name}
                </option>
              ))}
          </NativeSelect>
        </FormControl>

        <InputLabel variant="standard" htmlFor="uncontrolled-native">
          Target Action
        </InputLabel>
        <FormControl fullWidth className="formControl">
          <NativeSelect
            className="nativeSelect"
            value={form.target_action}
            onChange={(event) => handleSignalChange(event)}
            name="target_action"
            inputProps={{
              name: "target_action",
              id: "uncontrolled-native",
            }}
          >
            {targetActions?.length > 0 &&
              targetActions.map(({ name, action }) => (
                <option key={action} value={action}>
                  {name}
                </option>
              ))}
          </NativeSelect>
        </FormControl>
        {/* <TextField
            label="Target ID"
            value={form.target_device_id}
            onChange={(event) => handleSignalChange(event)}
          />
          <TextField
            label="Trigger Action"
            value={form.trigger_action}
            onChange={(event) => handleSignalChange(event)}
          />
          <TextField
            label="Trigger ID"
            value={form.trigger_id}
            onChange={(event) => handleSignalChange(event)}
          />
          <TextField
            label="Trigger Name"
            value={form.trigger_name}
            onChange={(event) => handleSignalChange(event)}
          />
          <TextField
            label="Trigger Num Action"
            value={form.trigger_num_actions}
            onChange={(event) => handleSignalChange(event)}
          /> */}
        <div>
          <Button variant="contained" onClick={handleAddSignal}>
            Add
          </Button>
        </div>
      </div>
    </Modal>
  );
};

export default AddSignalModal;
