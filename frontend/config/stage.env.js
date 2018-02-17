var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"staging"',
  WAMP_URL: '"wss://staging.orthogonal.space:8081/ws"'
})
