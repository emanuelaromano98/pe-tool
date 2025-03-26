import { useEffect, useState } from "react";
import { WS_URL } from "../api";

function useWebSocket() {
  const [status, setStatus] = useState("");

  // eslint-disable-next-line no-unused-vars
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    console.log("useWebSocket hook called");
    let ws;

    const connectWebSocket = () => {
      ws = new WebSocket(WS_URL);

      ws.onopen = () => {
        console.log("WebSocket Connected");
        setIsConnected(true);
        ws.send("ready"); // Send ready signal to server
      };

      ws.onmessage = (event) => {
        console.log("Received WebSocket message:", event.data);
        setStatus(event.data);
      };

      ws.onerror = (error) => {
        console.error("WebSocket error:", error);
        setIsConnected(false);
      };

      ws.onclose = () => {
        console.log("WebSocket Disconnected. Reconnecting in 1s...");
        setIsConnected(false);
        setTimeout(connectWebSocket, 1000); 
      };
    };

    connectWebSocket();

    return () => {
      if (ws) ws.close();
    };
  }, []);

  return status;
}

export default useWebSocket;
