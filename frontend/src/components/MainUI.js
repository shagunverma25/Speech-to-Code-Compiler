import React, { useState, useRef } from 'react';
import axios from 'axios';
import './MainUI.css'; // Make sure to create and include this

const MainUI = () => {
  const [recording, setRecording] = useState(false);
  const [language, setLanguage] = useState("python");
  const [response, setResponse] = useState({});
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const handleStartRecording = async () => {
    setResponse({});
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = event => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append("audio", audioBlob, "recorded.wav");
        formData.append("language", language);

        try {
          const res = await axios.post("http://localhost:5000/process", formData);
          setResponse(res.data);
        } catch (error) {
          console.error("❌ Error sending audio to backend:", error);
        }

        // Stop the mic stream cleanly
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorderRef.current.start();
      setRecording(true);
    } catch (err) {
      alert("🎙️ Unable to access microphone. Please check permissions.");
      console.error(err);
    }
  };

  const handleStopRecording = () => {
    mediaRecorderRef.current.stop();
    setRecording(false);
  };

  return (
    <div className="App">
      <h2>🎤 Speech-to-Code Compiler</h2>

      <div className="controls">
        <label><strong>Select Language:</strong></label>
        <select onChange={e => setLanguage(e.target.value)} value={language} disabled={recording}>
          <option value="python">Python</option>
          <option value="java">Java</option>
          <option value="c">C</option>
        </select>
      </div>

      <div>
        {!recording ? (
          <button onClick={handleStartRecording}>🎙️ Start Speaking</button>
        ) : (
          <button className="stop" onClick={handleStopRecording}>🛑 Stop & Compile</button>
        )}
      </div>

      {response.speech && (
        <div className="card">
          <h3>🗣️ Transcribed Speech</h3>
          <pre>{response.speech}</pre>
        </div>
      )}

      {response.tokens && (
        <div className="card">
          <h3>🧠 NLP Parsed Tokens</h3>
          <pre>{JSON.stringify(response.tokens, null, 2)}</pre>
        </div>
      )}

      {response.lexicalTokens && (
        <div className="card">
          <h3>🧮 Lexical Tokens (Compiler)</h3>
          <pre>{JSON.stringify(response.lexicalTokens, null, 2)}</pre>
        </div>
      )}

      {response.code && (
        <div className="card">
          <h3>💻 Generated Code</h3>
          <pre>{response.code}</pre>

          <h3>📤 Output</h3>
          <pre>{response.output || "✅ Code ran, but did not produce any output."}</pre>

          <a
            href={`http://localhost:5000/download/${response.fileName}`}
            download
            className="download-btn"
          >
            ⬇️ Download Code
          </a>
        </div>
      )}
    </div>
  );
};

export default MainUI;