import React from "react";

interface ContainerProps {
  children: React.ReactNode;
}

const Container: React.FC<ContainerProps> = ({ children }) => {
  return (
    <div className="xl-p-20 2xl-25 mx-auto w-3/4 px-10 md:px-15 xl:px-25">
      {children}
    </div>
  );
};

export default Container;
