import { useState } from "react";
import VideoLoadDisplay from "./VideoLoadDisplay";
import OptionsForm from "./OptionsForm";
import CaptionDisplay from "./CaptionDisplay";

interface Props {
    type: string,

    handleUrlSubmit: (
        ...args: any[]
    ) => Promise<void>;

    optionsState: { [key: string] : string }
    setOptionsState: React.Dispatch<React.SetStateAction<{ [key: string]: string}>>;
}


function UrlForm({ type, handleUrlSubmit, optionsState, setOptionsState }: Props) {
    //SETUP---------------
    //vars
    const [url, setUrl] = useState<string>('');
    const [videoUrl, setVideoUrl] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [caption, setCaption] = useState<string>('');

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
        <div className="flex flex-row items-center justify-center">

            {/* Title and desc */}
            <div className="w-1/2  flex flex-col justify-evenly items-center bg-blue-600 m-2 p-4 text-white rounded-3xl gap-5">
                <div className="blue-glass">
                    <h1 className="text-2xl font-bold underline">{headerTitle}</h1>
                    <p className="text-sm">{bodyText}</p>
                </div>
                
                {/* Custom Options */}
                <OptionsForm 
                    inputOptions={{"Voice Rate (1-250)" : "number",}} 
                    selectOptions={{"Voice Software": ["PyTTS", "ElevenLabs"], }}
                    onOptionsChange={(key, value) => {
                        //uses function to properly change vals, i.e., takes array of all previous values, ad
                        //only changes the one with the given key
                        setOptionsState((prev) => ({...prev, [key]: value}));
                    }}
                />

                {/* Take in URL for reddit video and submit */}
                <form className="blue-glass flex flex-col w-3/5 gap-2 justify-self-center items-center" 
                onSubmit={(e) => { handleUrlSubmit(e, setLoading, videoUrl, setVideoUrl, url, caption, setCaption, optionsState);}}
                >
                    <label className="w-full flex flex-col gap-2 items-center" >
                        <b>{type} URL:</b>
                        <input
                            className="text-black bg-white rounded w-3/4"
                            type="text"
                            id="redditUrl"
                            value={url}
                            onChange={e => setUrl(e.target.value)}
                        />
                    </label>
                    <button type="submit" className="blue-button">Submit</button>
                </form>
            </div>

            {/* Video/Load Display with Caption Display*/}
            <div className={`${loading || videoUrl !=="" ? "w-1/4" : "w-0 invisible"} bg-blue-600 rounded-3xl m-2 p-4 transition-all ease-in duration-1000 `}>
                <VideoLoadDisplay loading={loading} videoUrl={videoUrl}/>
                <div className={`${caption=="" ? "hidden" : ""}`}><CaptionDisplay caption={caption}/> {loading}</div>
            </div>
        </div>
        </>
    
    );
}

export default UrlForm