import { SimpleQueries, SimpleQuery } from "@jina-ai/jinajs";
import { MediaPreview } from "../common/MediaPreview";
import { TextPreview } from "../common/TextPreview";

export const QueryItem = ({
  query,
  selected,
  onClick,
}: {
  query: SimpleQuery;
  selected?: boolean;
  onClick?: () => void;
}) => {
  const { data, mimeType } = query;

  let isText = !mimeType.startsWith("data:") && !data.startsWith("data:");

  return (
    <div
      onClick={onClick}
      className={`max-h-48 relative flex-none flex items-center w-72 overflow-hidden cursor-pointer border border-gray-200 rounded p-4 mr-2 transition-all duration-200 ${
        selected ? "border-primary-500" : ""
      }`}
    >
      {isText ? (
        <TextPreview text={data} />
      ) : (
        <MediaPreview src={data} mimeType={mimeType} />
      )}
    </div>
  );
};

export const QuerySelector = ({
  queries,
  selectedIndex,
  select,
}: {
  queries?: SimpleQueries;
  selectedIndex: number;
  select: (index: number) => void;
}) => {
  return ( queries ?
    <div className="mb-4">
      <div className="mb-2 font-semibold text-xl">Queries</div>
      <div className="w-full overflow-auto whitespace-nowrap pb-2 flex flex-row">
        {queries.map((query, idx) => (
          <QueryItem
            query={query}
            selected={idx === selectedIndex}
            key={idx}
            onClick={() => select(idx)}
          />
        ))}
      </div>
    </div> : <></>
  );
};
