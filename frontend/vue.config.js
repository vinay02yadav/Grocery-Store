const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = defineConfig({
  transpileDependencies: [], // Set this array with specific package names or leave it empty to transpile all dependencies.
  configureWebpack: {
    plugins: [
      new webpack.ProvidePlugin({
        $: 'jquery',
        jquery: 'jquery',
        'window.jQuery': 'jquery',
        jQuery: 'jquery'
      }),
      // new CopyWebpackPlugin({
      //   patterns: [
      //     {
      //       from: 'src/views/dashboard/images',
      //       to: 'img',
      //       globOptions: {
      //         ignore: ['.*'],
      //       },
      //     },
      //   ],
      // }),
    ],
  },
});
