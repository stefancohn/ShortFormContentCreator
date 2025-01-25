# Short-Form Content Creator
If you are to contribute, please checkout your own branch, with the name being the feature you plan on implementing. Then push and send a PR. 
## Python Script 
- This is the "app", actually creates the videos
- Requires version 3.11, and a bunch of other packages that should be in requirements.txt. 
- The original version was developed on MacOS, hope this does not cause issues with other OS
- <em>You must create a config file with the appropriate credentials for the following APIs:</em>
  - PRAW
  - Elevenlabs API
- Might have to change file paths for the background video (or add  your own in the assets folder in the root), so keep that in mind if it doesn't work. 

## Front End
- Uses TSX React, so you'll need Node.js, and I believe it will work
- Uses Tailwind for CSS styling (https://nerdcave.com/tailwind-cheat-sheet)
- Run using ```npm run dev```

## Back End
- Uses Express.js within Node.js.
- Run using ```npm run dev```

The back end and front end must be running for the development environment to work. 
