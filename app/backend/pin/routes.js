const express = require('express');

const router = express.Router();

const Pins = require('../models/pins');

router.get('/',
    (req, res, next) => {
        Pins.find()
        .exec(function(err, data) {
            console.log(data)
            res.send(data);
        })
        .catch(err => next(err));
    }
);

router.post('/',
    (req, res, next) => {
        Pins.create({type: req.body.type, location: {latitude: req.body.location.latitude, longitude: req.body.location.longitude}});
        console.log(req.body.type);
    }
)

module.exports =  router;
