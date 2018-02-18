<template>
    <div md-align-trigger md-direction="bottom right" md-size="4" @open="focus" ref="user-menu">

        <md-button v-if="!logged_in" @click="openLogin()" class="user_menu_button">

            <md-avatar class="md-small">
                <img :src="get_gravatar()" alt="You are not logged in">
            </md-avatar>

            <span>Log In/Register</span>
        </md-button>

      <md-menu v-else md-menu-trigger md-direction="bottom left" ref="logoutMenu" class="md-dense" @keydown.esc.prevent="close" :md-offset-x="200" md-offset-y="64">
        <md-button md-menu-trigger>
          <md-avatar class="md-small">
              <img :src="get_gravatar(user.email)" :alt="user.email">
          </md-avatar>
              <span>{{ user.realname }}</span>
        </md-button>

        <md-menu-content>
            <md-button md-menu-trigger class="md-raised md-accent" @click="logout()">Logout</md-button>
        </md-menu-content>
      </md-menu>

        <md-dialog ref="login-dialog" class="md-dense">
            <md-list class="md-dense">
                <form class="loginform" novalidate @submit.stop.prevent="login" @keyup.enter="login()">
                    <md-input-container>
                        <label>Username</label>
                        <md-input class="logininput" ref="login_input_user" v-model="username"></md-input>
                    </md-input-container>
                    <md-input-container>
                        <label>Password</label>
                        <md-input class="logininput" ref="login_input_pass" type="password" v-model="password"></md-input>
                    </md-input-container>
                </form>

                <md-button class="md-raised md-primary" @click="login()">Login</md-button>

                <a @click="navigateRegistration()" to="/register" class="md-button md-raised">
                    Register
                </a>
            </md-list>
        </md-dialog>
    </div>
</template>

<style>
.logininput {
    margin: 5px;
}

.loginform {
    padding: 10px;
}

.user_menu_button{
    text-transform: none !important;
}
</style>

<script>
    export default {
        name: 'user-menu',
        data() {
            return {
                username: "",
                password: ""
            }
        },
        components: {
        },
        computed: {
            logged_in() {
                return this.$store.state.user.logged_in;
            },
            user() {
                return this.$store.state.user.user;
            }
        },
        methods: {
            openLogin() {
              this.$refs["login-dialog"].open();
            },
            openLogout() {
              this.$refs["logoutMenu"].open();
            },

            navigateRegistration() {
              this.$refs["login-dialog"].close();
              this.$router.push("/register");
            },

            login: function() {
                var self = this;
                if (!this.username) {
                    self.notify("Please enter your username or email address");
                    return;
                }
                if (!this.password) {
                    self.notify("Please enter your password");
                    return;
                }
                this.$wamp.call('session.login', [], {username: this.username, password: this.password}).then(function(res) {
                    if (res.success) {
                        self.$store.commit('login', res.user);
                        self.notify("Logged in successfully!");
                        self.$cookie.set('session', res.session, 30);
                        self.username = "";
                        self.password = "";
                        self.$refs["login-dialog"].close();
                    } else {
                        self.notify("Login failed!");
                    }
                });
            },
            logout: function() {
                var self = this;
                if (this.$store.state.user.logged_in) {
                    this.$wamp.call('session.logout', [], {session: this.$cookie.get('session')}).then(function(res) {
                        self.notify("Logged out successfully!");
                        self.$store.commit('logout');
                        self.$cookie.delete('session');
                        self.$router.push("/");
                    },
                    function(error) {
                        self.notify("Failed to logout.");
                    });
                } else {
                    self.notify("You are already logged out.");
                }
            },
            focus: function() {
                if (!this.$store.state.user.logged_in) {
                    this.$refs.login_input_user.$el.focus();
                }
            },
            close: function() {
                this.$refs.login_tab.$parent.close();
            },
            closeMenu: function() {
                this.$refs["logoutMenu"].close();
            }
        }
    }
</script>
