import React, { useCallback, useRef, useState } from "react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { LuSend } from "react-icons/lu";

interface ChatSubmitProps {
  sendMessage: (message: string) => void;
}

const ChatSubmit: React.FC<ChatSubmitProps> = ({ sendMessage }) => {
  const [message, setMessage] = useState<string>("");
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = useCallback(() => {
    sendMessage(message);
    setMessage("");
  }, [message])

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      handleSubmit(); // Call handleSubmit on Enter key press
    }
  };

  return (
    <div className="flex w-full max-w-xl items-center space-x-2">
      <Input
        ref={inputRef}
        value = {message}
        placeholder="What do you need help with?"
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown = {(e) => handleKeyDown(e)}
      />
      <Button
        type="submit"
        onClick={() => handleSubmit()}
        className="rounded-full"
        disabled={message == ""}
      >
        <LuSend />
      </Button>
    </div>
  );
};

export default ChatSubmit;
