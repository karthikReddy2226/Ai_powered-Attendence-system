import React, { useRef, useState } from "react";
import axios from "axios";

const DETECT_API = "http://127.0.0.1:8000/api/detect/"; // change as implemented

export default function LiveCapture() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [streaming, setStreaming] = useState(false);
  const [lastResult, setLastResult] = useState(null);

  const startCamera = async () => {
    if (streaming) return;
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      videoRef.current.play();
      setStreaming(true);
    } catch (err) {
      console.error("Camera error", err);
    }
  };

  const stopCamera = () => {
    const stream = videoRef.current?.srcObject;
    if (stream) {
      stream.getTracks().forEach((t) => t.stop());
      videoRef.current.srcObject = null;
    }
    setStreaming(false);
  };

  // capture frame and POST to backend
  const captureAndSend = async () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(async (blob) => {
      const form = new FormData();
      form.append("image", blob, "frame.jpg");

      try {
        const res = await axios.post(DETECT_API, form, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        setLastResult(res.data);
      } catch (err) {
        console.error("Upload error:", err);
      }
    }, "image/jpeg", 0.8);
  };

  return (
    <div style={{ padding: 20 }}>
      <h3>Live Capture</h3>
      <div>
        <video ref={videoRef} width="480" height="360" style={{ border: "1px solid #ccc" }} />
      </div>
      <div style={{ marginTop: 8 }}>
        <button onClick={startCamera} disabled={streaming}>Start Camera</button>
        <button onClick={captureAndSend} disabled={!streaming}>Capture & Send</button>
        <button onClick={stopCamera} disabled={!streaming}>Stop Camera</button>
      </div>
      <canvas ref={canvasRef} style={{ display: "none" }} />
      {lastResult && (
        <div style={{ marginTop: 12 }}>
          <strong>Last Response:</strong>
          <pre>{JSON.stringify(lastResult, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
