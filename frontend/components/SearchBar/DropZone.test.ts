/**
 * @jest-environment jsdom
 */

import { useRef } from "react";
import { act, renderHook } from "@testing-library/react-hooks";
import { useDropZone } from "./DropZone";

test("should start in a neutral state", () => {
  const { result: ref } = renderHook(() => useRef<HTMLDivElement>(null));
  const { result } = renderHook(() => useDropZone(ref.current));

  const { files, isDragging } = result.current;
  expect(files.length).toBe(0);
  expect(isDragging).toBe(false);
});

describe("useDropZone", () => {
  let domEvents: any = {};
  let dropZoneEvents: any = {};
  let hook: any;

  beforeEach(() => {
    domEvents = {};
    document.addEventListener = jest.fn((event, callback) => {
      domEvents[event] = callback;
    });

    dropZoneEvents = {};
    const dropAreaRef = {
      current: {
        addEventListener: jest.fn((event, callback) => {
          dropZoneEvents[event] = callback;
        }),
      },
    };

    const { result } = renderHook(() => useDropZone(dropAreaRef as any));
    hook = result;
  });

  it("should attach event listeners to the document", () => {
    const eventNames = Object.keys(domEvents);
    expect(eventNames.length).toEqual(5);
    expect(eventNames).toEqual([
      "dragenter",
      "dragleave",
      "dragend",
      "drop",
      "dragover",
    ]);
  });

  it("should attach a single drop event listener to the dropzone", () => {
    const eventNames = Object.keys(dropZoneEvents);
    expect(eventNames.length).toEqual(1);
    expect(eventNames).toEqual(["drop"]);
  });

  it("should show is dragging when items enter", () => {
    expect(hook.current.isDragging).toBe(false);
    act(() => {
      domEvents.dragenter();
    });
    expect(hook.current.isDragging).toBe(true);
  });

  it("should show not dragging after item leaves", () => {
    act(() => {
      domEvents.dragenter();
    });
    expect(hook.current.isDragging).toBe(true);
    act(() => {
      domEvents.dragleave({ clientX: 0, clientY: 0 });
    });
    expect(hook.current.isDragging).toBe(false);
  });

  it("should show not dragging after item is dropped", () => {
    act(() => {
      domEvents.dragenter();
    });
    expect(hook.current.isDragging).toBe(true);
    act(() => {
      domEvents.drop({ type: "drop" });
    });
    expect(hook.current.isDragging).toBe(false);
  });

  it("should grab the files from the drop event", () => {
    const file1 = new File([], "test-file.txt");
    const file2 = new File([], "test-file-2.txt");
    const files = [file1, file2];
    const dropEvent = {
      type: "drop",
      dataTransfer: { files },
      preventDefault: jest.fn(),
      stopPropagation: jest.fn(),
    };

    expect(hook.current.files.length).toBe(0);
    act(() => {
      dropZoneEvents.drop(dropEvent);
    });

    const { files: hookFiles } = hook.current;

    expect(dropEvent.preventDefault).toBeCalledTimes(1);
    expect(dropEvent.stopPropagation).toBeCalledTimes(1);
    expect(hookFiles.length).toBe(2);
    expect(hookFiles[0]).toEqual(file1);
    expect(hookFiles[1]).toEqual(file2);
  });
});
