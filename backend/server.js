const express = require("express");
const app = express();
const cors = require("cors");
const corsOption = {
    origin: "http://localhost:5173"
}

app.get("/api", (req, res) => {
    res.json({ message: "Hello from server!" });
});

app.listen(8080, ()=>{
    console.log("Server is running on port 8080");
});