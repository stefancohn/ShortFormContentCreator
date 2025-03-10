import { useEffect, useState } from 'react'
import axios, { AxiosResponse } from 'axios'
import UrlForm from './components/UrlForm.tsx'
import Navbar from './components/Navbar.tsx'

function RedditVidGenerate() {
  //pass to URL form, pass to OptionsForm
  //default are 2 kvps
  const [optionsState, setOptionsState] = useState<{ [key: string]: string }>({
      "Voice Rate": "125",
      "Voice Software": "PyTTS",
  });

  //handle url form submission 
  const handleUrlSubmit = async (
    e: React.FormEvent<HTMLFormElement>, 
    setLoading: React.Dispatch<React.SetStateAction<boolean>>, 
    videoUrl: string,
    setVideoUrl: React.Dispatch<React.SetStateAction<string>>,
    url: string,
    caption:string,
    setCaption: React.Dispatch<React.SetStateAction<string>>,
    optionsState: { [key: string] : string}
  ) => {
    e.preventDefault();
    setLoading(true);

    //if user tries to generator another video, reset videoUrl
    if (videoUrl !== "") {
      setVideoUrl("");
    }
    //same for caption
    if (caption !== "") {
      setCaption("");
    }

    //submit POST req
    try {
      //we send a POST req, the data being the url submitted, then we wait to receive a blob in the response (a vid)
      const resp: AxiosResponse = await axios.post("http://localhost:8080/reddit_video_api", { 
        url: url, options: optionsState
      }, {
          responseType: 'blob'
      });
      
      //when we receive response, load video
      console.log(resp.headers)
      const videoBlob = new Blob([resp.data], {type: 'video/mp4'});
      setVideoUrl(URL.createObjectURL(videoBlob))

      //get caption afterwards
      const captionResp = await axios.get('http://localhost:8080/caption');
      console.log(captionResp.data)
      //set caption
      setCaption(captionResp.data)
    } 
    catch (e) { 
      console.log(e) 
    }  //catch error
    finally { 
      setLoading(false) 
    } //set loading to false
  }

  //
  //FOR EXAMPLE PURPOSES

  const fetchAPI = async() => {
    const response = await axios.get('http://localhost:8080/api',)
    console.log(response)
  }

  //this like onLoad method
  useEffect(() => {
    fetchAPI();
  },[]);

  //END OF EXAMPLE
  //

  return (
    <>
      <Navbar/>
      <UrlForm type='Reddit' handleUrlSubmit={handleUrlSubmit} optionsState={optionsState} setOptionsState={setOptionsState}/>
    </>
  )
}

export default RedditVidGenerate