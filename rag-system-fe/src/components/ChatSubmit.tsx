import React, { useCallback, useRef, useState } from "react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { LuSend } from "react-icons/lu";

interface ChatSubmitProps {
  sendMessage: (message: string, userId: number) => void;
  userId: number | undefined;
}

const ChatSubmit: React.FC<ChatSubmitProps> = ({ sendMessage, userId }) => {
  const [message, setMessage] = useState<string>("");
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = useCallback(() => {
    if (!userId || !message) return;
    sendMessage(message, userId);
    setMessage("");
  }, [message]);

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      handleSubmit(); // Call handleSubmit on Enter key press
    }
  };

  return (
    <div className="flex w-full max-w-3xl items-center space-x-5">
      <Input
        className="bg-zinc-700 w-full text-white border-0 placeholder:text-zinc-400 focus-visible::outline-none focus-visible:ring-0 rounded-full text-lg px-7 py-7"
        ref={inputRef}
        value={message}
        placeholder="What do you need help with?"
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => handleKeyDown(e)}
      />
      <Button
        type="submit"
        onClick={() => handleSubmit()}
        className="rounded-full h-[56px] w-[56px]"
        disabled={message == ""}
      >
        <LuSend size = {56} />
      </Button>
    </div>
  );
};

export default ChatSubmit;
