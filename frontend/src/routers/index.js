import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/Home.vue'
import MainLayout from '../components/layouts/Main.vue'
import Join from '../components/Join.vue'
import Create from '../components/Create.vue'
import Register from '../components/Register.vue'
import Info from '../components/universe/Info.vue'
import Play from '../components/universe/Play.vue'
import GameLayout from '../components/layouts/Game.vue'

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
        },
        {
            path: '/universe/:name',
            component: GameLayout,
            children: [
                {
                    path: '',
                    name: 'info',
                    component: Info
                },
                {
                    path: 'play',
                    name: 'play',
                    component: Play
                }
            ]
        }
    ]
});
