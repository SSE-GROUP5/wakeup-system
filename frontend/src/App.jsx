import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import SignalsPage from "./pages/SignalsPage/SignalsPage";
import NavBar from "./components/NavBar/NavBar";
import Devices from "./pages/Devices/Devices";

function App() {

  return (
    <>
      <BrowserRouter>
        <NavBar />
        <Routes>
          <Route path="/signals" element={<SignalsPage />} />
          <Route path="/devices" element={<Devices />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
