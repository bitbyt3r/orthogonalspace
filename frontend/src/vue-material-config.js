import Vue from 'vue'
import VueMaterial from 'vue-material'


window.addEventListener('load', function () {
    Vue.use(VueMaterial)

    // red, pink, purple, deep-purple, indigo, blue, light-blue, cyan, teal, green, light-green, lime, yellow, amber, orange, deep-orange, brown, grey, blue-grey, white, black

    Vue.material.registerTheme({
      // default: {
      //   primary: 'indigo',
      //   accent: 'pink',
      //   warn: 'deep-orange',
      //   background: 'white'
      // },
      editor: {
        primary: 'teal',
        accent: 'red',
        warn: 'red',
        background: 'grey'
      },
      navbar: {
        primary: 'cyan'
      },
    })
})