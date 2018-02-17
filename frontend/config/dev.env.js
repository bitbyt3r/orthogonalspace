var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  WAMP_URL: '"ws://localhost:8080/ws"',
  ENABLE_RAVEN: 'false',
  //MAPS_KEY: '"AIzaSyAaAIWQLvisBO7liAUYZDOkDAX9zu_3Cmk"'
  //MAPS_KEY: '"AIzaSyBC1tnJU0JJEs9KCWyeFoZK54Y_9VOZWXo"'
  MAPS_KEY: '"Ari5N-T43juinFW8fmFVxLtlC0BpT-lSQOYlDPQoMNxBP5UJM8428a4FcEgarbQM"'
})
