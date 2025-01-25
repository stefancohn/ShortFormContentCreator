interface Props {
    loading: boolean,
    videoUrl: string,
}

function VideoLoadDisplay({ loading, videoUrl }: Props) {
    {/* Video/Load Display 
        Needs to be this way so that the font and bg smoothly expand onto screen*/}
    return (
        <>
        <div className={`${loading || videoUrl !== "" ? '' : 'invisible w-0 h-0'} transition-all ease-in duration-1000 flex flex-col gap-y-4 items-center justify-center  rounded-3xl p-4`}>
            {/* Conditional For When Loading */}
            <div>
                <h1 className={`text-white ${loading ? 'text-3xl' : 'text-0'} transition-all ease-in duration-1000 font-bold`}>Loading...</h1>
            </div>

            {/* Conditional For When Video is Loaded */}
            {videoUrl !== "" && 
                <>
                    <video controls className="w-48 rounded-xl shadow-xl ring-4 ring-blue-400 -mt-5">
                        <source src={videoUrl} type="video/mp4"></source>
                    </video>

                    <a href={videoUrl} download="ssfc.mp4" className="blue-button">Download Video</a>
                </>
            }
        </div> 
        </>
    )
}

export default VideoLoadDisplay;