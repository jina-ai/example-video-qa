import React, {
  ChangeEvent,
  MutableRefObject,
  useEffect,
  useRef,
  useState,
} from "react";
import { FilePreview } from "../common/FilePreview";

export function useDropZone(ref: MutableRefObject<HTMLDivElement | null>) {
  const [isDragging, setIsDragging] = useState(false);
  const [files, setFiles] = useState<File[]>([]);

  useEffect(() => {
    function showDrag(e: DragEvent) {
      setIsDragging(true);
    }
    function hideDrag(e: DragEvent) {
      const { clientX, clientY, type } = e;
      if (type === "drop" || (clientX === 0 && clientY === 0))
        setIsDragging(false);
    }
    function handleDrop(e: DragEvent) {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);
      if (!e.dataTransfer) return;
      const files = Array.from(e.dataTransfer.files);
      setFiles(files);
    }
    function doNothing(e: DragEvent) {
      e.preventDefault();
    }

    const element = ref.current;

    if (element) {
      element.addEventListener("drop", handleDrop);
    }

    document.addEventListener("dragenter", showDrag);
    document.addEventListener("dragleave", hideDrag);
    document.addEventListener("dragend", hideDrag);
    document.addEventListener("drop", hideDrag);
    document.addEventListener("dragover", doNothing);

    return () => {
      if (element) {
        element.removeEventListener("drop", handleDrop);
      }
      document.removeEventListener("dragenter", showDrag);
      document.removeEventListener("dragleave", hideDrag);
      document.removeEventListener("drop", hideDrag);
      document.removeEventListener("dragover", doNothing);
    };
  }, [ref]);

  return { isDragging, files };
}

export const DropZone = ({
  files,
  addFiles,
  removeFile,
}: {
  files: File[];
  addFiles: (files: File[]) => void;
  removeFile: (filename: string) => void;
}) => {
  const dropAreaRef = useRef<HTMLDivElement>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const { isDragging, files: droppedFiles } = useDropZone(dropAreaRef);

  useEffect(() => {
    addFiles(droppedFiles);
  }, [droppedFiles, addFiles]);

  function handleSelectFiles(e: ChangeEvent<HTMLInputElement>) {
    const fileList = e.target.files;
    if (fileList) addFiles(Array.from(fileList));
  }

  return (
    <div
      ref={dropAreaRef}
      className={`bg-white z-10 box-content ${
        isDragging || files.length ? "h-48" : "h-0"
      } none overflow-hidden absolute w-full bg-white -mb-7 rounded-md text-center mt-0.5 shadow-md transition-all duration-200`}
    >
      <div className="h-full w-full p-2 relative">
        {isDragging ? (
          <div
            className={`rounded absolute right-0 left-0 top-0 bottom-0 m-2 flex items-center border border-transparent ${
              isDragging
                ? "border-primary-500 bg-primary-500 bg-opacity-10 border-dashed"
                : ""
            }`}
          >
            <div className="mx-auto">Drop files here</div>
          </div>
        ) : (
          <div className="overflow-auto whitespace-nowrap flex flex-row h-full w-full pb-2">
            {files.map((file) => (
              <FilePreview
                key={file.name}
                file={file}
                remove={() => removeFile(file.name)}
              />
            ))}
          </div>
        )}
        <input
          type="file"
          ref={fileRef}
          style={{ display: "none" }}
          onChange={handleSelectFiles}
        />
      </div>
    </div>
  );
};
