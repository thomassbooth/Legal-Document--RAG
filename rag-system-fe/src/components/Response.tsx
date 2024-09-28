import React from 'react'


interface ResponseProps {
    type: number
    text : string
}


const Response: React.FC<ResponseProps> = ({ type, text }) => {
    return (
      <li className={`w-full flex ${type ? 'justify-end' : 'justify-start'} my-2`}>
        <div className={`max-w-[60vw] ${type ? "bg-zinc-700 rounded-full px-6 py-3 text-white" : ""}`}>
          {text}
        </div>
      </li>
    );
  };

export default Response