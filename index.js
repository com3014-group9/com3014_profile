const express = require("express")

const app = express()



app.get("/", (req,res) => {
    res.send("<h2>Profile Service - Under Construction</h2>");
});



const port = process.env.PORT || 3030;

app.listen(port, () => console.log('listening on ${port}'))

