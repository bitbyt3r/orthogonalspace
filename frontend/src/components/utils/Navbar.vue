<template>
    <div>
        <md-toolbar>
            <md-button class="md-icon-button md-hide-medium-and-up" @click="$refs.leftSidenav.toggle()">
                <md-icon>menu</md-icon>
            </md-button>

            <router-link class="md-title md-button md-primary" id="toolbar-title" to="/">
                Orthogonal Space
            </router-link>

            <user-menu class="md-hide-small" style="margin-left: auto"> </user-menu>
        </md-toolbar>

        <md-sidenav class="md-left" ref="leftSidenav">
            <md-toolbar class="md-large">
                <div class="md-toolbar-container">
                    <h3 class="md-title">Menu</h3>
                </div>
            </md-toolbar>

            <md-list>
                <md-list-item>
                    <router-link to="/" v-on:click.native="closeLeftSidenav">
                        <h3> <md-icon class="md-primary">home</md-icon> Orthogonal Space</h3>
                    </router-link>
                </md-list-item>
                <md-list-item>
                    <h3><user-menu></user-menu></h3>
                </md-list-item>
            </md-list>

        </md-sidenav>
    </div>
</template>
<style>
    .flew-grow-1 {
      flex-grow: 1;
    }
    #toolbar-title{
        text-transform: none !important;
    }
    .md-toolbar {
        z-index: 100;
    }
</style>


<script>
    import UserMenu from './UserMenu.vue';

    export default {
        name: 'navbar',
        computed: {
            logged_in() {
                return this.$store.state.user.logged_in;
            },
        },
        watch: {
        },
        methods: {
            closeLeftSidenav() {
                this.$refs.leftSidenav.close();
            }
        },
        mounted() {
            var self = this;
        },
        components: {
            UserMenu
        }
    }
</script>


