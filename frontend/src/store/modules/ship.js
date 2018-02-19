import Vue from 'vue'
import _ from 'lodash';

const state = {
    ship: {
        "name": "Unknown Name",
        "type": ""
    },
    shiptypes: {
    },
    ready: false
};
const getters = {
};
const actions = {
};
const mutations = {
    load_ship (state, ship) {
        state.ship = ship;
    },
    load_shiptypes (state, shiptypes) {
        state.shiptypes = shiptypes;
    },
    update_ship (state, updates) {
        _.assign(state.ship, updates);
    },
    update_ready (state, ready) {
        state.ready = ready;
    }
};

export default {
    state,
    getters,
    actions,
    mutations
};
