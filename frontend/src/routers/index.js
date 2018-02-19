import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/Home.vue'
import Register from '../components/Register.vue'

import GameLayout from '../components/layouts/Game.vue'
import MainLayout from '../components/layouts/Main.vue'

import CreateUniverse from '../components/universe/CreateUniverse.vue'
import Universe from '../components/universe/Universe.vue'

import CreateFaction from '../components/faction/CreateFaction.vue'
import Faction from '../components/faction/Faction.vue'

import CreateShip from '../components/ship/CreateShip.vue'
import Ship from '../components/ship/Ship.vue'
import ShipConfig from '../components/ship/ShipConfig.vue'

import Play from '../components/game/Play.vue'

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
                    path: 'universe/create',
                    name: 'createuniverse',
                    component: CreateUniverse
                },
                {
                    path: 'universe/:universeid/faction/create',
                    name: 'createfaction',
                    component: CreateFaction
                },
                {
                    path: 'universe/:universeid',
                    name: 'universe',
                    component: Universe
                },
                {
                    path: 'faction/:factionid/ship/create',
                    name: 'createship',
                    component: CreateShip
                },
                {
                    path: 'faction/:factionid',
                    name: 'faction',
                    component: Faction,
                },
                {
                    path: 'shipconfig/:shipid',
                    name: 'shipconfig',
                    component: ShipConfig
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
                    path: ':shipid',
                    name: 'play',
                    component: Play
                }
            ]
        }
    ]
});
