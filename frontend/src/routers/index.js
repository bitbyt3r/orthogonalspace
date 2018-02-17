import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/Home.vue'
import MainLayout from '../components/layouts/Main.vue'

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            component: MainLayout,
            children: [
                {
                    path: '',
                    name: 'home',
                    component: Home
                }
            ]
        }
    ]
});
