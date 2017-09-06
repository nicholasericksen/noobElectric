const express = require('express');

const router = express.Router();

const Experiments = require('./models');

router.get('/',
    (req, res, next) => {
        // console.log("req", req);
        // console.log("MODELS", models);
        Experiments.find()
        .exec(function(err, data) {
            console.log('ERROR', err);
            console.log(data)
            res.send(data);
        })
        .catch(err => next(err));
    }
);

router.get('/status', (req, res, next) => {
    res.send({ status: 'ok' });
});

// router.get('/status',
//     res.send('OK');
// );

// router.post('/',
//     (req, res, next) => {
//         models.create({type: req.body.type, location: {latitude: req.body.location.latitude, longitude: req.body.location.longitude}});
//         console.log(req.body.type);
//     }
// )

module.exports =  router;
