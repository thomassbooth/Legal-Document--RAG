import React from "react";

interface ContainerProps {
  children: React.ReactNode;
}

const Container: React.FC<ContainerProps> = ({ children }) => {
  return (
    <div className="xl-p-15 2xl-20 min-h-screen mx-auto w-full p-5 md:p-10 xl:px-20">
      {children}
    </div>
  );
};

export default Container;
