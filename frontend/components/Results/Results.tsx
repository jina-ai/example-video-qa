import React, {ComponentType, ReactNode, useState} from "react";
import {SimpleQueries, SimpleResult, SimpleResults} from "@jina-ai/jinajs";
import {QuerySelector} from "./Queries";
import VideoPlayer from "../VideoPlayer";

type CustomResultItemProps = {
    result: SimpleResult
}
export type ICustomResultItem = ComponentType<CustomResultItemProps>

export type ResultsProps = {
    results: SimpleResults[];
    queries?: SimpleQueries;
    CustomResultItem?: ICustomResultItem
    classNames?: string
};

export const Results = ({ results, queries, CustomResultItem, classNames }: ResultsProps) => {
    const [selectedIndex, setSelectedIndex] = useState(0);

    const hasResults = results.length > 0;
    const selectedResults = results[selectedIndex];

    return (
        <div className="relative max-w-full overflow-hidden">
            <QuerySelector
                queries={queries}
                selectedIndex={selectedIndex}
                select={setSelectedIndex}
            />

            {hasResults ? (
                <div className={`flex flex-wrap justify-center 2xl:justify-start ${classNames}`}>
                    {selectedResults.map((result, idx) => (
                        <VideoPlayer result={result} key={idx} />
                    ))}
                </div>
            ) : (
                <></>
            )}
        </div>
    );
};
