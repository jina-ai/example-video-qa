import { useState } from 'react'
import JinaClient, { RawDocumentData, SimpleResults, SimpleQueries, AnyObject, SimpleResult } from "@jina-ai/jinajs";
import Results from "../components/Results";
import { Spinner } from "../components/Spinner"
import { SearchBar } from "../components/SearchBar";
import VideoPlayer from '../components/video/VideoPlayer';
import {Header} from '../components/Header';

const VIDEO_SEARCH_ENDPOINT = 'http://localhost:45678'

export default function GamingShowcase() {
    const [queries, setQueries] = useState<SimpleQueries>([]);
    const [results, setResults] = useState<SimpleResults[]>([]);
    const [searching, setSearching] = useState(false)
    const [searchedDocumentName, setSearchedDocumentName] = useState("")

    const jinaClient = new JinaClient(VIDEO_SEARCH_ENDPOINT, undefined, false, undefined, customReponseSerializer)


    async function search(...documents: RawDocumentData[]) {
        setSearching(true);
        if (typeof documents[0] === "string") {
            setSearchedDocumentName(documents[0])
        } else {
            setSearchedDocumentName(documents[0].name)
        }
        const { results, queries } = await jinaClient.search(documents[0])
        setSearching(false);
        setResults(results);
        setQueries(queries);
    }
    return (
        <div>
            <Header />
            <div className="w-full overflow-y-auto p-8">
                <SearchBar searching={searching} search={search} placeholder={"Search video"}/>
                {searching ? (
                    <Searching />
                ) : (
                        queries.length?<>
                            <h2 className="font-bold text-xl mb-3">
                                Results:
                </h2>
                            <Results classNames="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" results={results}/>
                        </>:""
                    )}
            </div>
        </div>
    )
}

const customReponseSerializer = (rawResponse: AnyObject) => {
    const docs = rawResponse.data.data;
    const results: SimpleResults[] = [];
    const queries: SimpleQueries = [];
    docs.forEach((doc: any) => {
        queries.push({
            data: doc.text || doc.uri,
            mimeType: doc.mimeType,
        });
        const { matches } = doc;
        results.push(
            matches.sort((match1: any, match2: any) => match1.scores.relevance_score.value - match2.scores.relevance_score.value).map(({ scores, text, uri, tags, mimeType }: any) => {
                const score = scores.relevance_score.value
                    ? scores.relevance_score.value
                    : scores.score?.value;
                return {
                    data: tags?.glb_path || text || uri,
                    url: uri,
                    timestamp: tags.timestamp,
                    mimeType,
                    score,
                } as SimpleResult;
            })
        );
    });
    return { queries, results };
}

const Searching = () => (
    <div className="mx-auto text-3xl py-36 flex flex-row items-center text-primary-500">
        <Spinner />
        <span className="animate-pulse">Searching...</span>
    </div>
);
