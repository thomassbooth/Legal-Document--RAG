import React, { Dispatch, SetStateAction, useState } from "react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { TbPlugConnected } from "react-icons/tb";

interface WSConnectionProps {
    onConnect: Dispatch<SetStateAction<WebSocket | null>>  // Pass WebSocket back to parent
  }


const WSConnection:React.FC<WSConnectionProps> = ({onConnect}) => {
  const [userId, setUserId] = useState<number>();

  const handleConnect = () => {
    if (userId !== undefined) {
      const ws = new WebSocket("ws://localhost:8000/ws");
      onConnect(ws);  // Pass the WebSocket connection to parent
    }
  };

  return (
    <div className="flex space-x-2">
      <Input
        className="bg-zinc-700 w-full text-white border-0 placeholder:text-zinc-400 focus-visible::outline-none focus-visible:ring-0 rounded-full text-lg px-7 py-7"
        value={userId}
        placeholder="User ID"
        onChange={(e) => setUserId(parseInt(e.target.value))}
      />
      <Button
        type="submit"
        onClick={() => handleConnect()}
        className="rounded-full h-[56px] w-[56px]"
        disabled={userId == undefined}
      >
        <TbPlugConnected size={56} />
      </Button>
    </div>
  );
};

export default WSConnection;
