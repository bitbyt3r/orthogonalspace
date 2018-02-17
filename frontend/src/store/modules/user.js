import Vue from 'vue'

const state = {
    logged_in: false,
    user: ""
};
const getters = {
};
const actions = {
};
const mutations = {
    login (state, user) {
        state.logged_in = true;
        state.user = user;
    },
    logout (state) {
        state.logged_in = false;
        state.user = null;
    },
    update_user (state, user) {
        state.user = user;
    }
};

export default {
    state,
    getters,
    actions,
    mutations
};
