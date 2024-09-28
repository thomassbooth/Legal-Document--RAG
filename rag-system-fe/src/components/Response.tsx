import React from 'react'


interface ResponseProps {
    type: number
    text : string
}


const Response: React.FC<ResponseProps> = ({ type, text }) => {
    return (
      <li className={`w-full flex ${type ? 'justify-end' : 'justify-start'} my-2`}>
        <div className="max-w-[60vw] p-2 bg-gray-200 rounded-lg">
          {text}
        </div>
      </li>
    );
  };

export default Response