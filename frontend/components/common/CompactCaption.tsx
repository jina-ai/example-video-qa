import React from "react";

export const CompactCaption = ({ text }: { text: string }) => {
  return (
    <div className="overflow-ellipsis whitespace-nowrap overflow-hidden">
      {text}
    </div>
  );
};
