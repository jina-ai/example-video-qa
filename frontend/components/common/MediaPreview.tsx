import React from "react";

export const MediaPreview = ({
  mimeType,
  src,
  rounded = true,
}: {
  mimeType?: string;
  src: string;
  rounded?: boolean;
}) => {
  if (mimeType?.startsWith("image") || src.startsWith("data:image"))
    return (
      <img
        src={src}
        alt="Image"
        className={`min-h-12 min-2-12 h-80 max-h-full max-w-full mx-auto${
          rounded ? " rounded" : ""
        }`}
      />
    );

  if (mimeType?.startsWith("video") || src.startsWith("data:video"))
    return (
      <video
        src={src}
        controls
        muted
        autoPlay
        loop
        className={`min-h-12 min-w-12 max-h-full max-w-full mx-auto ${
          rounded ? " rounded" : ""
        }`}
      />
    );

  if (mimeType?.startsWith("audio") || src.startsWith("data:audio"))
    return <audio controls src={src} className="w-full m-1" />;

  // TODO: fallback option
  return null;
};
