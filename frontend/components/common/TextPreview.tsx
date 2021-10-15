export const TextPreview = ({
  text,
  clampLines = 2,
}: {
  text: string;
  size?: "sm" | "md" | "lg";
  font?: "regular" | "mono";
  clampLines?: number;
}) => {
  return (
    <div>
      <span className="jina-text-item overflow-hidden overflow-ellipsis">
        {text}
      </span>
      <style jsx>
        {`
          .jina-text-item {
            display: -webkit-box;
            -webkit-line-clamp: ${clampLines};
            -webkit-box-orient: vertical;
            overflow: hidden;
          }
        `}
      </style>
    </div>
  );
};
