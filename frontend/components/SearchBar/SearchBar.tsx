import React, { useCallback, useRef, useState } from "react";
import { SearchInput } from "./SearchInput";
import { DropZone } from "./DropZone";
import { RawDocumentData } from "@jina-ai/jinajs";

const SearchButton = ({ onClick }: { onClick: () => void }) => {
  return (
    <div
      className="text-white px-6 h-12 font-medium cursor-pointer flex justify-center items-center text-lg"
      onClick={onClick}
    >
      Search
    </div>
  );
};

type SearchBarProps = {
  search: (...documents: RawDocumentData[]) => void;
  searching: boolean;
  placeholder?: string
};

export const SearchBar = ({ search, searching, placeholder }: SearchBarProps) => {
  const inputRef = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<File[]>([]);

  function handleSearch() {
    const text = inputRef.current?.value;
    if (text) search(text, ...files);
    else search(...files);
    setFiles([]);

    if (inputRef.current) inputRef.current.value = "";
  }

  const addFiles = useCallback((files: File[]) => {
    setFiles((prev) => {
      return [...prev, ...files];
    });
  }, []);

  function removeFile(filename: string) {
    setFiles((prev) => {
      return prev.filter((file) => file.name !== filename);
    });
  }

  return (
    <div className="p-0.5 w-full bg-primary-500 rounded-lg flex flex-row">
      <div className="relative flex-1 h-12">
        <SearchInput
          searching={searching}
          inputRef={inputRef}
          addFiles={addFiles}
          onEnter={handleSearch}
          placeholder={placeholder}
        />
        <DropZone files={files} addFiles={addFiles} removeFile={removeFile} />
      </div>
      <SearchButton onClick={handleSearch} />
    </div>
  );
};
