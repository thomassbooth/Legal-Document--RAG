"use client";

import ChatSubmit from "@/components/ChatSubmit";
import Container from "@/components/Container";
import Response from "@/components/Response";
import Thinking from "@/components/Thinking";
import { ScrollArea } from "@/components/ui/scroll-area";
import WSConnection from "@/components/WSConnection";
import useWebSocket from "@/hooks/useWebSocket";
import { useEffect, useState } from "react";

export default function Home() {
  const {
    ws,
    messageHistory,
    thinking,
    sendMessage,
    setWs,
    userId,
    setUserId
  } = useWebSocket();

  
  return (
    <div className="flex flex-col h-screen items-center justify-between py-10">
      <WSConnection onConnect={setWs} userId={userId} setUserId = {setUserId}/>
      <section className="w-full flex flex-col items-center">
        <div className="mt-6 w-full">
          <ScrollArea className="w-full h-[80vh] py-10">
            <Container>
              {ws ? (
                <div>
                  <ul className="flex gap-2 w-full flex-wrap">
                    {messageHistory.map((msg, index) => (
                      <Response
                        key={index}
                        type={msg.userType}
                        text={msg.data}
                      />
                    ))}
                  </ul>
                  {thinking && <Thinking />}
                </div>
              ) : (
                <Response type={0} text="Please connect as your userid..." />
              )}
            </Container>
          </ScrollArea>
        </div>
        <ChatSubmit sendMessage={sendMessage} userId = {userId}/>
      </section>
    </div>
  );
}
