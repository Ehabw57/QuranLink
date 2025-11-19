const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  // Build output goes to the server public directory so the server can serve the SPA
 outputDir: '../server/public',
  // Serve assets from root when hosted by the server
  publicPath: '/',
})

