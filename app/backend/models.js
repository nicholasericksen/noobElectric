var mongoose = require('mongoose');

var experimentSchema = new mongoose.Schema({
    title: String
    // description: String,
    // // date: String,
    // data: {
    //     images: String,
    //     histograms: {
    //         measurements: {
    //             h: [[Number, Number]],
    //             v: [[Number, Number]],
    //             p: [[Number, Number]],
    //             m: [[Number, Number]]
    //         },
    //         stokes: {
    //             s1: [[Number, Number]],
    //             s2: [[Number, Number]]
    //         }
    //     }
    // }
});
console.log("MODEL SCHEMA");
module.exports = mongoose.model('Experiment', experimentSchema);
