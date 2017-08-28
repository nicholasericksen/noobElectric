var mongoose = require('mongoose');

var pinSchema = new mongoose.Schema({
    type: String,
    location: {
        latitude: Number,
        longitude: Number
    }
});

module.exports = mongoose.model('Pin', pinSchema);
