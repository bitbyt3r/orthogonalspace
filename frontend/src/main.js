import 'aframe'

import Vue from 'vue'
import router from './routers'
import store from './store/index.js'
import App from './App.vue'
import VeeValidate from 'vee-validate'
import TreeView from "vue-json-tree-view"
import VueKindergarten from 'vue-kindergarten'
import spacePerimeter from './perimeters/spacePerimeter.js'
import VueCookie from 'vue-cookie'

import './vue-material-config.js'
import './vue-wamp.config.js'
import './vue-configs.js'
import 'mixins/index.js'

import 'vue-material-home/vue-material.css'
import './style.css'
import _ from 'lodash'
import VueResource from 'vue-resource'

Vue.config.productionTip = false

var bus = new Vue();

window.addEventListener('load', function () {
  Vue.use(TreeView)
  Vue.use(VeeValidate)
  Vue.use(VueKindergarten, {
      child: (store) => {
          return store.state.user
      }
  })
  Vue.use(VueCookie)
  Vue.use(VueResource)

  window.vue = new Vue({
    router,
    store,
    el: '#app',
    perimeters: [
        spacePerimeter
    ],
    render: h => h(App)
  })
})
