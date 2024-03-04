import axios from "axios";
import { BACKEND_URL } from "../constants";

export const api = axios.create({
  baseURL: BACKEND_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

const healthCheck = async () => {
  try {
    const response = await api.get("/health");
    return response.data;
  } catch (error) {
    return error;
  }
}


const addTrigger = async (trigger) => {
  try {
    const response = await api.post("/triggers", trigger);
    return response.data;
  } catch (error) {
    return error;
  }
}

const getTrigger = async (id) => {
  try {
    const response = await api.get(`/triggers/${id}`);
    return response.data;
  } catch (error) {
    return error;
  }
}

export const updateTrigger = async (id, trigger) => {
  try {
    const response = await api.put(`/triggers/${id}`, trigger);
    return response.data;
  } catch (error) {
    return error;
  }
}


const getTriggers = async () => {
  try {
    const response = await api.get("/triggers");
    return response.data;
  } catch (error) {
    return error;
  }
}


const getTargets = async () => {
  try {
    const response = await api.get("/target_devices");
    return response.data;
  } catch (error) {
    return error;
  }
}

const addTarget = async (target) => {
  try {
    const response = await api.post("/target_devices", target);
    return response.data;
  } catch (error) {
    return error;
  }
}

const deleteTarget = async (id) => {
  try {
    const response = await api.delete(`/target_devices/${id}`);
    return response.data;
  } catch (error) {
    return error;
  }
}

const addSignal = async (signal) => {
  try {
    const response = await api.post("/signals/set", signal);
    return response.data;
  } catch (error) {
    console.log(error);
    return error;
  }
}

const getSignals = async () => {
  try {
    const response = await api.get("/signals");
    console.log(response.data);
    return response.data?.signals || [];
  } catch (error) {
    return error
  }
}

const getSignalsForUser = async (userId) => {
  try {
    const response = await api.get(`/signals/users/${userId}`);
    return response.data;
  } catch (error) {
    return error
  }
}

const createUser = async (user) => {
  try {
    const response = await api.post("/users", user);
    return response.data;
  } catch (error) {
    return error
  }
}

const getUsers = async () => {
  try {
    const response = await api.get("/users");
    return response.data;
  } catch (error) {
    return error
  }
}

const getUser = async (id) => {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    return error
  }
}

const deleteUser = async (id) => {
  try {
    const response = await api.delete(`/users/${id}`);
    return response.data;
  } catch (error) {
    return error
  }
}

export const apiService = {
  signals: {
    addSignal,
    getSignals,
    getSignalsForUser
  },

  triggers: {
    addTrigger,
    getTrigger,
    updateTrigger,
    getTriggers
  },

  targets: {
    addTarget,
    deleteTarget,
    getTargets,
  },

  users: {
    createUser,
    getUsers,
    getUser,
    deleteUser
  },

  healthCheck

}