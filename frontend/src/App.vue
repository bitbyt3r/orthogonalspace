<template>
    <div id="app-inner">
        <router-view> </router-view>

        <md-snackbar :md-position="'bottom center'" ref="snackbar" :md-duration="4000">
            <span v-html="message"></span>
        </md-snackbar>
        <md-snackbar :md-position="'bottom right'" ref="savebar" :md-duration="Infinity">
            <span>Now saving...</span>
        </md-snackbar>
    </div>
</template>

<style>
    #app-inner {
        height: 100vh;
    }
</style>

<script>
    export default {
        data() {
            return {
                message: ''
            }
        },
        mounted() {
            var self = this;
            var session = this.$cookie.get('session');
            if (session) {
                this.$wamp.call('session.renew', [], {session: session}).then(
                    function(res) {
                        if (res.success) {
                            self.$store.commit('login', res.user);
                        }
                    },
                    function(error) {
                        console.log('Failed to renew old session');
                    }
                );
            }
        }
    }
</script>
