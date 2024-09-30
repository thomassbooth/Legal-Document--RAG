import { getUserHistory } from "@/actions/getUserHistory";
import { useEffect, useRef, useState } from "react";

const useWebSocket = () => {
  const [ws, setWs] = useState<WebSocket | null>(null); // WebSocket can now be set dynamically
  const [messageHistory, setMessageHistory] = useState<Message[]>([]);
  const [thinking, setThinking] = useState<boolean>(false);
  const [userId, setUserId] = useState<number | undefined>(undefined);
  const streamRef = useRef<boolean>(false);

  // when user name changes, we need to refresh the history
  useEffect(() => {
    if (!userId) return;
    async function fetchHistory() {
      const history = await getUserHistory(userId as number);
      setMessageHistory([...history["history"]]);
    }
    fetchHistory();
  }, [ws]);

  // Set up WebSocket connection
  useEffect(() => {
    if (!ws) return;

    ws.onmessage = (event) => {
      // Process incoming messages and update state
      console.log(event.data)
      setThinking(false);
      // we send a start+ to tell us were expecting a stream so setup the value
      if (event.data === "start+") {
        streamRef.current = true;
        setMessageHistory((prevHistory) => [
          ...prevHistory,
          { userType: 0, data: "" }, // Start a new message
        ]);
        return;
      } else if (event.data === "end+") {
        streamRef.current = false;
        return;
      }
      // if we are in a stream, append the data to the last message
      if (streamRef.current) {
        setMessageHistory((prevHistory) => [
          ...prevHistory.slice(0, prevHistory.length - 1),
          { userType: 0, data: prevHistory[prevHistory.length - 1].data + event.data },
        ]);
        console.log("Received message");
      }
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed");
    };

    // Clean up WebSocket on unmount
    return () => {
      console.log("Cleaning up WebSocket connection");
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [ws]); // Depend on the WebSocket connection

  // Send a message to the WebSocket server
  const sendMessage = (message: string, userId: number) => {
    //check the websocket is ready and there is acutally a message
    if (ws && ws.readyState === WebSocket.OPEN && message) {
      setThinking(true);
      ws.send(JSON.stringify({ userid: userId, message }));

      setMessageHistory((prevHistory) => [
        ...prevHistory,
        { userType: 1, data: message },
      ]);
    }
  };

  return {
    ws,
    messageHistory,
    thinking,
    sendMessage,
    setWs,
    userId,
    setUserId,
  }; // Expose setWs to set the WebSocket dynamically
};

export default useWebSocket;
