import { TrashIcon } from "@heroicons/react/outline";
import { XIcon } from "@heroicons/react/solid";
import React, { useEffect, useState } from "react";
import { CompactCaption } from "./CompactCaption";
import { MediaPreview } from "./MediaPreview";

export const FilePreview = ({
  file,
  remove,
}: {
  file: File;
  remove?: () => void;
}) => {
  const [src, setSrc] = useState("");

  useEffect(() => {
      const reader = new FileReader();
      reader.onload = (e: any) => {
        setSrc(e.target.result);
      };
      reader.readAsDataURL(file);
  }, [file]);

  return (
    <div className="flex-none h-full bg-gray-50 w-72 flex flex-col rounded relative mr-2 select-none">
      <div className="flex-1 overflow-hidden flex items-center px-2 pt-2">
        <MediaPreview mimeType={file.type} src={src} />
      </div>
      <div className="p-1 px-2 flex flex-row items-center">
        <CompactCaption text={file.name} />
        <div className="flex-1 text-right">
          {remove && (
            <TrashIcon
              className="h-4 inline cursor-pointer text-gray-700 hover:text-black"
              onClick={remove}
            />
          )}
        </div>
      </div>
    </div>
  );
};
