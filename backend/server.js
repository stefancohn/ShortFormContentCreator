//express config
const express = require("express");
const app = express();
app.use(express.json());
path = require('path');

//cors
const cors = require("cors");
const corsOption = {
    origin: "http://localhost:5173"
};
app.use(cors(corsOption));


//test get req
app.get("/api", (req, res) => {
    res.json({ message: "Hello from server!" });
});


//handle reddit_video_api
app.post("/reddit_video_api", (req, res) => {
    const {url}  = req.body;
    console.log("Received URL:", url);

    //call python script
    const spawn = require("child_process").spawn;
    const pythonProcess = spawn('python3',["../videoGenerator/generate_video.py", url]);

    //debug logs
    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    //on end of child process
    pythonProcess.on('close', (code) => {
        console.log(`child process exited with ${code}`);
        
        //send video file on successful script
        if (code === 0) {
            const videoPath = path.join(__dirname, "../videoGenerator/outputs/video.mp4");

            res.setHeader('Content-Type', 'video/mp4');
            res.sendFile(videoPath);
        } 
        else {
            res.status(500).json({ message: "Error in generating video" });
        }
    });

});

app.listen(8080, ()=>{
    console.log("Server is running on port 8080");
});