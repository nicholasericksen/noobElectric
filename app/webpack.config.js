var webpack = require('webpack');
var path = require('path');

module.exports = {
  entry: [
    "./public/js/index.jsx"
  ],
  output: {
    path: path.join(__dirname, '/public/static'),
    filename: "bundle.js"
  },
  module: {
    rules: [
        {
            test: /\.less$/,
            use: [{
                loader: "style-loader" // creates style nodes from JS strings
            }, {
                loader: "css-loader" // translates CSS into CommonJS
            }, {
                loader: "less-loader" // compiles Less to CSS
            }]
        },
      {
        test: /\.js?$/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'react']
        },
        exclude: /node_modules/
    },
    {
        test: /\.jsx$/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'react']
        },
        exclude: /node_modules/
    },
    // { test: /\.css$/, loader: "style-loader!css-loader", exclude: /node_modules/ },
    // {
    //     test: /\.less$/,
    //     loader: "style-loader!less-loader!less",
    //     exclude: /node_modules/
    // }
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx']
},
  plugins: [
  ]
};
