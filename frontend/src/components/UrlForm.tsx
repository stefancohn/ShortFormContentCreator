import { useState } from "react";
import axios, { AxiosResponse } from "axios";

interface Props {
    apiUrl: string,
    type: string,
}


function UrlForm({ apiUrl, type }: Props) {
    //SETUP---------------
    //vars
    const [url, setUrl] = useState<string>('');
    const [videoUrl, setVideoUrl] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);

    //handle url form submission 
    const handleUrlSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);

        //if user tries to generator another video, reset videoUrl
        if (videoUrl !== "") {
            setVideoUrl("");
        }

        //submit POST req
        try {
            //get binary video, blob
            const resp: AxiosResponse = await axios.post(apiUrl, { url: url }, {
                responseType: 'blob'
            });
            
            //when we receive response, load video
            console.log(resp.headers)
            const videoBlob = new Blob([resp.data], {type: 'video/mp4'});
            setVideoUrl(URL.createObjectURL(videoBlob))
            
        } 
        catch (e) { 
            console.log(e) 
        }  //catch error
        finally { 
            setLoading(false) 
        } //set loading to false
    }



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