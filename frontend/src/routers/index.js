import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/Home.vue'
import MainLayout from '../components/layouts/Main.vue'
import Join from '../components/Join.vue'
import Create from '../components/Create.vue'
import Register from '../components/Register.vue'

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
                },
                {
                    path: 'join',
                    name: 'join',
                    component: Join
                },
                {
                    path: 'create',
                    name: 'create',
                    component: Create
                },
                {
                    path: 'register',
                    name: 'register',
                    component: Register
                }
            ]
        }
    ]
});
