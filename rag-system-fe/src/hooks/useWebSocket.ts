import { useEffect, useState } from "react";

const useWebSocket = () => {
  const [ws, setWs] = useState<WebSocket | null>(null); // WebSocket can now be set dynamically
  const [messageHistory, setMessageHistory] = useState<Message[]>([]);
  const [thinking, setThinking] = useState<boolean>(false);

  // when user name changes, we need to refresh the history
  useEffect(() => {
    setMessageHistory([]);
  }, [ws]);

  useEffect(() => {
    if (!ws) return;

    // Set up WebSocket event listeners
    ws.onopen = () => {
      console.log("Connected to WebSocket server");
    };

    ws.onmessage = (event) => {
      // Process incoming messages and update state
      setThinking(false);
      setMessageHistory((prevHistory) => [
        ...prevHistory,
        { user: 0, data: event.data },
      ]);
      console.log("Received message");
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed");
    };

    // Clean up WebSocket on unmount
    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [ws]); // Depend on the WebSocket connection

  // Send a message to the WebSocket server
  const sendMessage = (message: string) => {
    //check the websocket is ready and there is acutally a message
    if (ws && ws.readyState === WebSocket.OPEN && message) {
      setThinking(true);
      ws.send(JSON.stringify({ userid: 1, message }));

      setMessageHistory((prevHistory) => [
        ...prevHistory,
        { user: 1, data: message },
      ]);
    }
  };

  return { ws, messageHistory, thinking, sendMessage, setWs }; // Expose setWs to set the WebSocket dynamically
};

export default useWebSocket;
