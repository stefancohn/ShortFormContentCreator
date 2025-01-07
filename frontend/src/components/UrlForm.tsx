import { useState } from "react";
import axios, { AxiosResponse } from "axios";

interface Props {
    apiUrl: string
}


function UrlForm({ apiUrl }: Props) {
    //SETUP---------------
    //vars
    const [url, setUrl] = useState('');

    //handle url form submission 
    const handleUrlSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        //submit POST req
        try {
            const resp = await axios.post(apiUrl, { url: url })
            console.log(resp.data);
        } catch (e) { console.log(e) }  //catch error
    }



    //CONSTRUCTION OF COMPONENT---------------
    return (
        <form className="flex flex-col space-y-4" onSubmit={(e) => handleUrlSubmit(e)}>
            <label className="self-center" >
                {/* URL field */}
                Reddit URL:
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
    );
}

export default UrlForm