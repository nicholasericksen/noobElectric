var express = require('express');
var path = require('path');
var bodyParser = require('body-parser');

var mongoose = require('mongoose');
var config = require('./config');
var Pin = require('./models/pins');

var app = express();

mongoose.connect(config.database);
mongoose.connection.on('error', function() {
    console.info('Error: Could not connect to the database!');
});

app.set('port', process.env.PORT || 4444);
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
app.use(express.static(path.join('../frontend/public')));

const pinRoutes = require('./pin/routes');

app.use('/api', pinRoutes);

app.listen(app.get('port'), function() {
    console.log('Express listening on port ' + app.get('port'));
});
