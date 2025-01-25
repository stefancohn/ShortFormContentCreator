import { useEffect } from 'react'
import axios, { AxiosResponse } from 'axios'
import UrlForm from './components/UrlForm.tsx'
import Navbar from './components/Navbar.tsx'

function RedditVidGenerate() {
  //handle url form submission 
  const handleUrlSubmit = async (
    e: React.FormEvent<HTMLFormElement>, 
    setLoading: React.Dispatch<React.SetStateAction<boolean>>, 
    videoUrl: string,
    setVideoUrl: React.Dispatch<React.SetStateAction<string>>,
    apiUrl: string,
    url: string,
    caption:string,
    setCaption: React.Dispatch<React.SetStateAction<string>>,
    options:string,
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
        const resp: AxiosResponse = await axios.post(apiUrl, { url: url, options: options}, {
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

  const fetchAPI = async() => {
    const response = await axios.get('http://localhost:8080/api',)
    console.log(response)
  }

  //this like onLoad method
  useEffect(() => {
    fetchAPI();
  },[]);

  return (
    <>
      <Navbar/>
      <UrlForm apiUrl={"http://localhost:8080/reddit_video_api"} type='Reddit' handleUrlSubmit={handleUrlSubmit}/>
    </>
  )
}

export default RedditVidGenerate