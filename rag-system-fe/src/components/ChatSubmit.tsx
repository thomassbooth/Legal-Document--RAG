import React from "react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { LuSend } from "react-icons/lu";

const ChatSubmit = () => {
  return (
    <div className="flex w-full max-w-xl items-center space-x-2">
      <Input placeholder="What do you need help with?" />
      <Button type="submit" className = 'rounded-full'>
        <LuSend />
      </Button>
    </div>
  );
};

export default ChatSubmit;
