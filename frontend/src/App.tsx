import { useEffect } from 'react'
import axios from 'axios'
import UrlForm from './components/UrlForm.tsx'

function App() {
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
      <UrlForm apiUrl={"http://localhost:8080/reddit_video_api"} type='Reddit' />
    </>
  )
}

export default App