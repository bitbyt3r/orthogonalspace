import Vue from 'vue'
import VueWamp from 'vue-wamp'

Vue.use(VueWamp, {
  debug: true,
  lazy_open: false,
  url: process.env.WAMP_URL,
  realm: 'realm1',
  onopen: function(session, details) {
    console.log('WAMP connected', session, details);
  },
  onclose: function(reason, details) {
    console.log('WAMP closed: ' + reason, details);
  }
});
