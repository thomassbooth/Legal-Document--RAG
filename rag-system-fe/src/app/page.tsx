"use client";

import ChatSubmit from "@/components/ChatSubmit";
import Container from "@/components/Container";
import Response from "@/components/Response";
import Thinking from "@/components/Thinking";
import { ScrollArea } from "@/components/ui/scroll-area";
import WSConnection from "@/components/WSConnection";
import useWebSocket from "@/hooks/useWebSocket";
import { useEffect, useRef, useState } from "react";

export default function Home() {
  const scrollRef = useRef(null)
  const {
    ws,
    messageHistory,
    thinking,
    sendMessage,
    setWs,
    userId,
    setUserId
  } = useWebSocket();

  useEffect(() => {
    if (scrollRef.current) {
      // @ts-expect-error - scrollRef is not typed
      scrollRef.current.scrollTo({
        // @ts-expect-error - scrollHeight is not typed
        top: scrollRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messageHistory]);
  
  return (
    <div className="flex flex-col h-screen items-center justify-between pt-6">
      <WSConnection onConnect={setWs} userId={userId} setUserId = {setUserId}/>
      <section className="w-full flex flex-col items-center">
        <div className="mt-6 w-full">
          <ScrollArea ref = {scrollRef} className="w-full h-[75vh] py-10">
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
        <span className = 'py-2'>built by Thomas Booth</span>
      </section>
    </div>
  );
}
