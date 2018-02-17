<template>
    <div>
        <md-toolbar>
            <md-button class="md-icon-button" @click="$refs.leftSidenav.toggle()">
                <md-icon>menu</md-icon>
            </md-button>

            <router-link class="md-title md-button md-primary" id="toolbar-title" to="/">
                Orthogonal Space
            </router-link>

            <router-link class="md-button md-primary" to="/spaces">
                <md-icon>web</md-icon> Spaces
            </router-link>

            <a class="md-button md-primary" href="//help.irc.umbc.edu" target="_blank">
                <md-icon>live_help</md-icon> Help
            </a>

            <router-link class="md-button md-primary" to="/about">
                <md-icon>info</md-icon> About
            </router-link>

            <div class="flew-grow-1"></div>
            <div v-if="num_users > 0">
              +{{ num_users }}
            </div>
            <user-menu> </user-menu>
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
                        <h3> <md-icon class="md-primary">home</md-icon> Home</h3>
                    </router-link>
                </md-list-item>
                <md-list-item>
                    <router-link to="/spaces" v-on:click.native="closeLeftSidenav">
                        <h3> <md-icon class="md-primary">web</md-icon> Spaces</h3>
                    </router-link>
                </md-list-item>
                <md-list-item href="//help.irc.umbc.edu" target="_blank">
                      <h3> <md-icon class="md-primary">live_help</md-icon> Help</h3>
                </md-list-item>
                <md-list-item>
                    <router-link to="/about" v-on:click.native="closeLeftSidenav">
                        <h3> <md-icon class="md-primary">info</md-icon> About</h3>
                    </router-link>
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
        data() {
            return {
                num_users: 0,
                current_sub: null
            }
        },
        watch: {
            $route: function() {
                var self = this;
                this.$wamp.unsubscribe(this.current_sub);
                this.$wamp.subscribe(this.$route.path, function (args, kwArgs, details) {}, {}).then(function(sub) {
                    self.current_sub = sub;
                });
                this.refresh_user_count();
            }
        },
        methods: {
            closeLeftSidenav() {
                this.$refs.leftSidenav.close();
            },
            refresh_user_count() {
                var self = this;
                if (self.$route.path.startsWith('/space/')) {
                    self.$wamp.call('wamp.subscription.lookup', [self.$route.path]).then(function(res) {
                        self.$wamp.call('wamp.subscription.count_subscribers', [res]).then(function(num_users) {
                            self.num_users = num_users - 1;
                        });
                    });
                } else {
                    self.num_users = 0;
                }
            }
        },
        mounted() {
            var self = this;
            self.$wamp.subscribe(self.$route.path, function (args, kwArgs, details) {}, {}).then(function(sub) {
                self.current_sub = sub;
            });
            self.$wamp.subscribe('wamp.subscription.on_subscribe', self.refresh_user_count, {});
            self.$wamp.subscribe('wamp.subscription.on_unsubscribe', self.refresh_user_count, {});
            self.refresh_user_count();
        },
        components: {
            UserMenu
        }
    }
</script>


