"use client";

import ChatSubmit from "@/components/ChatSubmit";
import Container from "@/components/Container";
import Response from "@/components/Response";
import { ScrollArea } from "@/components/ui/scroll-area";
import PreviousMap from "postcss/lib/previous-map";
import { useEffect, useState } from "react";

export default function Home() {
  const [ws, setWs] = useState<WebSocket>();
  const [messageHistory, setMessageHistory] = useState<Message[] | []>([{user: 0, data: "Hey! How can I help you today?"}]);
  const [thinking, setThinking] = useState<boolean>(false);

  useEffect(() => {
    // Initialize WebSocket connection to FastAPI server
    const socket = new WebSocket("ws://localhost:8000/ws");

    // Set up event listeners
    socket.onopen = () => {
      console.log("Connected to WebSocket server");
      setWs(socket);
    };

    socket.onmessage = (event) => {
      // Add new received message to state
      setThinking(false)
      setMessageHistory((prevHistory) => [
        ...prevHistory,
        { user: 0, data: event.data },
      ]);
      console.log("got message");
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

  const sendMessage = (message: string) => {
    if (ws && ws.readyState === WebSocket.OPEN && message) {
      setThinking(true)
      ws.send(JSON.stringify({userid: 1, message: message}));
      
      setMessageHistory((prevHist) => [
        ...prevHist,
        { user: 1, data: message },
      ]);
    }
    
  };

  return (
    <div className="flex flex-col items-center justify-bottom">
      <h1 className="text-2xl font-bold mb-4">RAG-System Takehome</h1>
      <div className="mt-6 w-full">
        <h2 className="text-xl font-semibold">Message History</h2>
        <ScrollArea className="w-full h-[75vh]">
          <Container>
          <ul className="flex gap-2 w-full flex-wrap">
            {messageHistory.map((msg, index) => (
              <Response key={index} type={msg.user} text={msg.data} />
            ))}
          </ul>
          {thinking && <Response type={0} text="Thinking..." />}
          </Container>
        </ScrollArea>
      </div>
      <ChatSubmit sendMessage={sendMessage}/>
    </div>
  );
}
