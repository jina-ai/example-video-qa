import React from "react"
import ReactPlayer from "react-player"

type VideoPlayerProps = {
    result: any
}
export default function VideoPlayer ({result}: VideoPlayerProps) {
    return (
        <ReactPlayer url={`${result.url}&t=${result.timestamp}s`} width="100%" height="20rem" controls />
    )
}