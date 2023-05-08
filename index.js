//const express = require("express")

//const app = express()


//app.get("/", (req,res) => {
 //   res.send("<h2>Profile Service - Under Construction</h2>");
//});


//const port = process.env.PORT || 3030;

//app.listen(port, () => console.log('listening on ${port}'))


const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

app.use(bodyParser.urlencoded({ extended: true }));

// Route to create a new user profile
app.post('/profile/create_user', (req, res) => {
  const user_id = req.body.user_id;
  return res.status(200).json({ user_id });
});

// Route to update a user's profile picture
app.post('/profile/update_user_pfp', (req, res) => {
  const user_id = req.body.user_id;
  const pfp = req.body.pfp;
  if (!user_id || !pfp) {
    return res.status(400).json({ error: 'Bad request, try again' });
  }
  return res.status(200).json({ pfp });
});

// Route to get a user's followers
app.get('/profile/get_followers', (req, res) => {
  const user_id = req.query.user_id;
  if (!user_id) {
    return res.status(400).json({ error: 'Bad request, try again' });
  }
  const followers = [
    { user_id: '1', user_name: 'user_1', pfp: null },
    { user_id: '2', user_name: 'user_2', pfp: null },
    { user_id: '3', user_name: 'user_3', pfp: null },
  ];
  return res.status(200).json(followers);
});

app.listen(port, () => console.log(`Listening on port ${port}`));
