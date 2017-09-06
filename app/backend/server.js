var express = require('express');
var path = require('path');
var bodyParser = require('body-parser');

var mongoose = require('mongoose');
var config = require('./config');
var Experiments = require('./models');

var app = express();

mongoose.connect(config.database);
mongoose.connection.on('error', function() {
    console.info('Error: Could not connect to the database!');
});

app.set('port', process.env.PORT || 4444);
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
app.use(express.static(path.join('../frontend/public')));

const routes = require('./routes');

app.use('/api', routes);

app.listen(app.get('port'), function() {
    console.log('Express listening on port ' + app.get('port'));
});
