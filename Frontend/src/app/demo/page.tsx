"use client";

import React, { useCallback, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootDispatch, RootState } from "@/store";
import { clearCallState, makeOutgoingCall } from "@/store/slices/outgoingCallSlice";
import { toast } from "sonner";


const DemoPage = () => {
  const dispatch = useDispatch<RootDispatch>();
  const { loading, error, lastResponse } = useSelector(
    (state: RootState) => state.outgoingCall
  );

  const [to, setTo] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!to || !message) {
      toast.error("Please fill both 'to' and 'message' fields");
      return;
    }

    try {
      await dispatch(makeOutgoingCall({ to, message })).unwrap();
      setMessage("");
    } catch (err) {
      toast.error("Call failed: " + String(err));
      console.error("Call failed:", err);
    }
  };

    

  return (
    <div className="flex items-center justify-center min-h-screen bg-black text-white p-6">
      <div className="w-full max-w-md bg-zinc-900/60 p-6 rounded-lg shadow-lg">
        <h1 className="text-2xl font-bold mb-4 text-center">Demo Call</h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-zinc-300 mb-1">To (phone)</label>
            <input
              value={to}
              onChange={(e) => setTo(e.target.value)}
              placeholder="+91xxxxxxxxxx"
              className="w-full px-3 py-2 rounded-md bg-black/40 border border-zinc-700 text-white text-sm"
            />
          </div>

          <div>
            <label className="block text-sm text-zinc-300 mb-1">Message</label>
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Your voice message text..."
              className="w-full px-3 py-2 rounded-md bg-black/40 border border-zinc-700 text-white text-sm h-28 resize-none"
            />
          </div>

          <div className="flex items-center justify-between gap-2">
            <button
              type="submit"
              disabled={loading}
              className={`flex-1 px-4 py-2 rounded-md text-white font-medium transition ${
                loading ? "opacity-60 cursor-not-allowed bg-green-700" : "bg-green-600 hover:bg-green-700"
              }`}
            >
              {loading ? "Calling..." : "Call"}
            </button>

          
          </div>

          {error && <div className="text-sm text-red-400 mt-2">Error: {String(error)}</div>}
          {lastResponse && (
            <div className="text-sm text-green-300 mt-2">
              Success: {JSON.stringify(lastResponse)}
            </div>
          )}
        </form>
      </div>
    </div>
  );
};

export default DemoPage;
