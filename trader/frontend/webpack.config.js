const webpack = require('webpack');
const path = require('path');

module.exports = {
    entry: './js/index.js',
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /(node_modules)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env', '@babel/preset-react']
                    }
                }
            },
            {
                test: /\.css$/,
                use: ['css-loader', 'style-loader']
            }
        ]
    },
    devServer: {
        contentBase: path.join(__dirname, "public/"),
        port: 3000,
        hotOnly: true
    },
    plugins: [
        new webpack.ProgressPlugin(),
        new webpack.HotModuleReplacementPlugin()
    ],
    optimization: {
        minimize: false
    },
    mode: "development"
};