"use client";

import { useEffect, useRef, useState } from "react";

export default function VoiceAIDashboard() {
  const wsRef = useRef<WebSocket | null>(null);
  const [finalTranscript, setFinalTranscript] = useState("");
  const [completeTranscript, setCompleteTranscript] = useState("");

  useEffect(() => {
    wsRef.current = new WebSocket("ws://localhost:8000/ws/client");

    wsRef.current.onopen = () => {
      console.log("✅ Frontend connected to backend WebSocket");
    };

    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "final_transcript") {
        console.log("✅ Final:", data.text);
        setFinalTranscript(data.text);
      } else if (data.type === "partial_transcript") {
        console.log("🎯 Complete:", data.text.transcript);
        setCompleteTranscript(data.text.transcript);
      }
    };

    return () => {
      wsRef.current?.close();
    };
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 p-4 text-white">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2 flex items-center justify-center gap-3">
            🎤 Voice AI Dashboard
          </h1>
          <p className="text-purple-200">
            Real-time voice conversation with AI
          </p>
        </div>

        {/* Live Transcripts */}
        <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-6 mb-6 space-y-4">
          <h3 className="text-xl font-bold text-yellow-300">📝 Transcripts</h3>

          <div>
            <p className="text-sm text-purple-300">✅ Final Transcript:</p>
            <p className="text-lg font-semibold text-white">
              {finalTranscript}
            </p>
          </div>

          <div>
            <p className="text-sm text-purple-300">🎯 Complete Turn:</p>
            <p className="text-lg font-semibold text-green-300">
              {completeTranscript}
            </p>
          </div>
        </div>

        {/* Setup Instructions (unchanged) */}
        {/* ... your existing setup instructions ... */}
      </div>
    </div>
  );
}
