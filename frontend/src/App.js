import React from "react";
import AttendanceDashboard from "./components/AttendanceDashboard";
import LiveCapture from "./components/LiveCapture";

function App() {
  return (
    <div>
      <h1 style={{ textAlign: "center" }}>AI Attendance System</h1>
      <div style={{ display: "flex", gap: 20, justifyContent: "center" }}>
        <LiveCapture />
        <AttendanceDashboard />
      </div>
    </div>
  );
}

export default App;
