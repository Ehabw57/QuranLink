const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = defineConfig({
  transpileDependencies: true,
  // Build output goes to the server public directory so the server can serve the SPA
  outputDir: '../server/public',
  // Serve assets from root when hosted by the server
  publicPath: '/',
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src'),
      },
    },
  },
})

