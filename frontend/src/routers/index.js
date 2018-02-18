import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/Home.vue'
import MainLayout from '../components/layouts/Main.vue'
import Join from '../components/Join.vue'
import Create from '../components/Create.vue'
import Register from '../components/Register.vue'
import Info from '../components/universe/Info.vue'
import Play from '../components/universe/Play.vue'
import CreateFaction from '../components/universe/CreateFaction.vue'
import CreateShip from '../components/universe/CreateShip.vue'
import Factions from '../components/universe/Factions.vue'
import Ships from '../components/universe/Ships.vue'
import Faction from '../components/universe/Faction.vue'
import Ship from '../components/universe/Ship.vue'
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
                    path: 'universes',
                    name: 'universes',
                    component: Universes
                },
                {
                    path: 'universe/create',
                    name: 'createuniverse',
                    component: CreateUniverse
                },
                {
                    path: 'universe/:universeid',
                    name: 'universe',
                    component: Universe
                },
                {
                    path: 'factions',
                    name: 'factions',
                    component: Factions
                },
                {
                    path: 'faction/create',
                    name: 'createfaction',
                    component: CreateFaction
                },
                {
                    path: 'faction/:factionid',
                    name: 'faction',
                    component: Faction
                },
                {
                    path: 'ships',
                    name: 'ships',
                    component: Ships
                },
                {
                    path: 'ship/create',
                    name: 'createship',
                    component: CreateShip
                },
                {
                    path: 'ship/:shipid',
                    name: 'ship',
                    component: Ship
                },
                {
                    path: 'register',
                    name: 'register',
                    component: Register
                }
            ]
        },
        {
            path: '/play',
            component: GameLayout,
            children: [
                {
                    path: 'ship/:shipid',
                    name: 'play',
                    component: Play
                }
            ]
        }
    ]
});
