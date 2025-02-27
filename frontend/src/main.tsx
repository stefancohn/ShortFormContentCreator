import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import RedditVidGenerate from './RedditVidGenerate.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RedditVidGenerate />
  </StrictMode>,
)
