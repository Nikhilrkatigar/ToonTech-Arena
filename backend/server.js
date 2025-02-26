require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Connect to MongoDB
mongoose.connect(process.env.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log('MongoDB Connected'))
  .catch(err => console.log(err));

// Team Schema
const TeamSchema = new mongoose.Schema({
    teamName: String,
    players: [String],
    teamHeadPhone: String,
    departments: [String]
});

const Team = mongoose.model('Team', TeamSchema);

// Route to handle registration
app.post('/register', async (req, res) => {
    const { teamName, players, teamHeadPhone, departments } = req.body;

    try {
        const newTeam = new Team({ teamName, players, teamHeadPhone, departments });
        await newTeam.save();
        res.status(201).json({ message: 'Registration successful!' });
    } catch (error) {
        res.status(500).json({ message: 'Error registering team', error });
    }
});

// Start Server
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
