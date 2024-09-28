"use client";

import ChatSubmit from "@/components/ChatSubmit";
import { Textarea } from "@/components/ui/textarea";
import { useEffect, useState } from "react";

export default function Home() {
  const [ws, setWs] = useState(null);
  const [message, setMessage] = useState("");
  const [messageHistory, setMessageHistory] = useState([]);

  useEffect(() => {
    // Initialize WebSocket connection to FastAPI server
    const socket = new WebSocket("ws://localhost:8000/ws");

    // Set up event listeners
    socket.onopen = () => {
      console.log("Connected to WebSocket server");
      //@ts-expect-error yes
      setWs(socket);
    };

    socket.onmessage = (event) => {
      // Add new received message to state
      //@ts-expect-error yes
      
      setMessageHistory((prevHistory) => [...prevHistory, event.data]);
      console.log('got message')
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socket.onclose = () => {
      console.log("WebSocket connection closed");
    };

    // Cleanup WebSocket on unmount
    return () => {
      if (socket.readyState === WebSocket.OPEN) {
        socket.close();
      }
    };
  }, []);

  const sendMessage = () => {
    //@ts-expect-error yes
    if (ws && ws.readyState === WebSocket.OPEN && message) {
      //@ts-expect-error yes
      ws.send(message);
      console.log('sent')
      setMessage(""); // Clear input after sending
    }
  };

  return (
    <div className="flex flex-col items-center justify-bottom">
      <h1 className="text-2xl font-bold mb-4">WebSocket Client</h1>

      <button
        onClick={sendMessage}
        className="px-4 py-2 bg-blue-500 text-white"
      >
        Send Message
      </button>

      <div className="mt-6">
        <h2 className="text-xl font-semibold">Messages Received:</h2>
        <ul className="flex gap-2 w-full flex-wrap">
          {messageHistory.map((msg, index) => (
            <li key={index}>{msg}</li>
          ))}
        </ul>
      </div>
      <ChatSubmit/>
    </div>
  );
}
