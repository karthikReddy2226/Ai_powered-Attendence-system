import React, { useEffect, useState } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8000/api/attendance/";

export default function AttendanceDashboard() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [polling, setPolling] = useState(true);

  const fetchRecords = async () => {
    setLoading(true);
    try {
      const res = await axios.get(API);
      setRecords(res.data);
    } catch (err) {
      console.error("Fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecords();
    if (!polling) return;
    const id = setInterval(fetchRecords, 3000); // poll every 3s
    return () => clearInterval(id);
  }, [polling]);

  return (
    <div style={{ padding: 20 }}>
      <h2>Live Attendance</h2>
      <button onClick={() => setPolling(!polling)}>
        {polling ? "Stop Live" : "Start Live"}
      </button>
      {loading ? <p>Loading…</p> : null}
      <table border="1" cellPadding="8" style={{ marginTop: 12 }}>
        <thead>
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {records.length === 0 ? (
            <tr><td colSpan="3">No records</td></tr>
          ) : (
            records.map((r, i) => (
              <tr key={r.id || i}>
                <td>{i + 1}</td>
                <td>{r.name}</td>
                <td>{new Date(r.time).toLocaleString()}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
