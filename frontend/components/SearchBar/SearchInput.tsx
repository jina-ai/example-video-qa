import React, {
  ChangeEvent,
  KeyboardEvent,
  MutableRefObject,
  useRef,
} from "react";
const jinaIcon = "/assets/magnifyingGlass.svg";
const crossIcon = "/assets/cross.svg"
const fileIcon = "/assets/file.svg";
const searchingIcon = "/assets/searching.gif";

type InputRef = MutableRefObject<HTMLInputElement | null>;

export const SearchInput = ({
  inputRef,
  addFiles,
  onEnter,
  searching,
  placeholder = "Search"
}: {
  inputRef: InputRef;
  addFiles: (files: File[]) => void;
  onEnter?: () => void;
  searching: boolean;
  placeholder?: string
}) => {
  const fileRef = useRef<HTMLInputElement>(null);

  function triggerFileSelect() {
    fileRef.current?.click();
  }

    function deleteInput() {
        if (inputRef.current) inputRef.current.value = ""
    }

  function handleSelectFiles(e: ChangeEvent<HTMLInputElement>) {
    const fileList = e.target.files;
    if (fileList) addFiles(Array.from(fileList));
  }

  function handleKeyPress(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter" && onEnter) {
      return onEnter();
    }
  }

  return (
    <div className="flex flex-row items-center h-full bg-white rounded-md">
      <div className="absolute ml-4 h-6 w-6 flex">
        <img
          src={searching ? searchingIcon : jinaIcon}
          alt="jina"
        />
      </div>
      <div className="absolute right-0 mr-4 mb-0 flex pl-4 h-6">
        <img
            src={crossIcon}
            alt="image"
            className="cursor-pointer"
            onClick={deleteInput}
        />
        <div className='border-l border-gray-400 mx-2'/>

        <img
          src={fileIcon}
          alt="image"
          className="cursor-pointer"
          onClick={triggerFileSelect}
        />
        <input
          type="file"
          multiple
          ref={fileRef}
          style={{ display: "none" }}
          onChange={handleSelectFiles}
        />
      </div>
      <input
        className={`rounded-md w-full h-full pl-16 border-none outline-none focus:shadow-lg transition-all duration-200 ${
          searching ? "bg-primary-500 bg-opacity-10 animate-pulse" : ""
        }`}
        disabled={searching}
        placeholder={searching ? "Searching..." : placeholder}
        ref={inputRef}
        onKeyPress={handleKeyPress}
      />
    </div>
  );
};
