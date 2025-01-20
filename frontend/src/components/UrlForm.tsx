import { useState } from "react";
import axios, { AxiosResponse } from "axios";
import VideoLoadDisplay from "./VideoLoadDisplay";
import OptionsForm from "./OptionsForm";

interface Props {
    apiUrl: string,
    type: string,
    handleUrlSubmit: (
        e: React.FormEvent<HTMLFormElement>, 
        setLoading: React.Dispatch<React.SetStateAction<boolean>>, 
        videoUrl: string,
        setVideoUrl: React.Dispatch<React.SetStateAction<string>>,
        apiUrl: string,
        url: string,
    ) => Promise<void>;
}


function UrlForm({ apiUrl, type, handleUrlSubmit }: Props) {
    //SETUP---------------
    //vars
    const [url, setUrl] = useState<string>('');
    const [videoUrl, setVideoUrl] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);

    const headerTitle : string = "Reddit Video Generator";
    const bodyText : string = `This is a Reddit Video Generator. It will generate a video with a Reddit card in the beginning.
        Then, a TTS program will read the post body along with subtitles on the screen.
        The background will feature gameplay.\n
        The longer the post, the longer the load time. 
        Please enter a Reddit URL to generate a video.
    `;



    //CONSTRUCTION OF COMPONENT---------------
    return (
        <>

        {/* Take in URL for reddit video */}
        <form className="flex flex-col space-y-4" onSubmit={(e) => handleUrlSubmit(e)}>
            <label className="self-center" >
                {type} URL:
                <input
                    className="bg-blue-500 rounded ml-4"
                    type="text"
                    id="redditUrl"
                    value={url}
                    onChange={e => setUrl(e.target.value)}
                />

            </label>
            <button type="submit">Submit</button>
        </form>

        {/* Conditional For When Video is Loaded */}
        {videoUrl !== "" && 
            <>
                <video controls width="40%" height="60%">
                    <source src={videoUrl} type="video/mp4"></source>
                </video>

                <a href={videoUrl} download="ssfc.mp4">Download Video</a>
            </>
        }

        {/* Conditional For When Loading */}
        {loading && 
            <h1>Loading...</h1>
        }
        </>
    
    );
}

export default UrlForm