import Vue from 'vue'
import vueConfig from 'vue-config'

const configs = {
  baseURL: '',
  isLoggingEnabled: true,
  ReCaptchaKey: '6Ld7GjMUAAAAAK75l-fwTLidLLJDL3D7BOYaHfuD'
}

Vue.use(vueConfig, configs)