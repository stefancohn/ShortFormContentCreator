//express config
const express = require("express");
const app = express();
app.use(express.json());

//cors
const cors = require("cors");
const corsOption = {
    origin: "http://localhost:5173"
};
app.use(cors(corsOption));

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

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
    pythonProcess.on('close', (code) => {
        console.log(`child process exited with ${code}`);
    });

    res.json({ message: "VidGenerated" });

});

app.listen(8080, ()=>{
    console.log("Server is running on port 8080");
});