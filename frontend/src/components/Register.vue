<template>
    <div>
        <h1>Register</h1>
        <form novalidate @submit.stop.prevent="submit">
            <md-input-container required="true" :class="{'md-input-invalid': errors.has('username')}">
                <label>Username</label>
                <md-input name="username" v-model="username" v-validate="'required'"></md-input>
                <span v-show="errors.has('username')">{{ errors.first('username') }}</span>
            </md-input-container>

            <md-input-container required="true" :class="{'md-input-invalid': errors.has('fullname')}">
                <label>Full Name</label>
                <md-input name="fullname" v-model="fullname" v-validate="'required'"></md-input>
                <span v-show="errors.has('fullname')">{{ errors.first('fullname') }}</span>
            </md-input-container>

            <md-input-container :class="{'md-input-invalid': errors.has('email')}">
                <label>Email</label>
                <md-input name="email" v-model="email" v-validate="'required|email'"></md-input>
                <span v-show="errors.has('email')">{{ errors.first('email') }}</span>
            </md-input-container>

            <md-input-container required="true" :class="{'md-input-invalid': errors.has('password')}">
                <label>Password</label>
                <md-input name="password" type="password" v-model="password" v-validate="'required|min:6'"></md-input>
                <span v-show="errors.has('password')">{{ errors.first('password') }}</span>
            </md-input-container>

            <input class="hidden" name="recaptcha" v-model="recaptcha" v-validate="'required'" >
            <vue-recaptcha ref="recaptcha" @verify="onRecaptchaVerify" @expired="onRecaptchaExpired" sitekey="6Ld4BEcUAAAAADhoUFlpd088I_xaE_VtJ6UZgb4A"></vue-recaptcha>
            <span class="md-input-invalid" v-show="errors.has('recaptcha')">You must check the ReCaptcha</span>
            <br />

            <span>
                <md-checkbox type="checkbox" ref="terms-checkbox" id="terms" name="terms" v-model="terms" v-validate="'required'" class="md-primary">
                  I agree to follow the <a href="" id="terms-dialog" @click.stop.prevent="openTerms()">terms of service</a>
                </md-checkbox>

                <br/>
                <span vclass="md-input-invalid" v-show="errors.has('terms')">You must agree to the terms.</span>
            </span>
            <br />

            <md-layout md-row>
                <md-layout md-flex="12" md-align="center">
                    <md-button class="md-primary md-raised" :disabled="false" @click="submit">Register</md-button>
                </md-layout>
            </md-layout>
        </form>
        <md-dialog md-open-from="#terms-dialog" md-close-to="#terms-dialog" ref="terms">
          <md-dialog-title>Terms of Use</md-dialog-title>

          <md-dialog-content><terms></terms></md-dialog-content>

          <md-dialog-actions>
            <md-button class="md-primary" @click="closeTerms(false)">Cancel</md-button>
            <md-button class="md-primary" @click="closeTerms(true)">Ok</md-button>
          </md-dialog-actions>
        </md-dialog>
    </div>
</template>

<script>
    import VueRecaptcha from 'vue-recaptcha';
    import Terms from './TOS';

    export default {
        name: 'register',
        components: {
            VueRecaptcha,
            Terms
        },
        data() {
            return {
                username: "",
                fullname: "",
                email: "",
                password: "",
                terms: "",
                recaptcha: ""
            };
        },
        methods: {
            openTerms() {
                this.$refs['terms'].open();
            },
            closeTerms(check) {
                this.$refs['terms-checkbox'].checked = check;
                this.$refs['terms'].close();
            },
            submit: function() {
                var self = this;
                this.$validator.validateAll()
                .then((isValidated) => {
                    if(!isValidated) return;

                    self.$wamp.call('user.register', [], {
                        username: self.username,
                        fullname: self.fullname,
                        email: self.email,
                        password: self.password,
                        recaptcha: self.recaptcha,
                        terms: self.terms
                    }).then(function(res) {
                        if (!res.success) {
                            self.notify("Error in account creation: " + res.reason);
                            throw new Error("Error in account creation");
                            return;
                        }

                        self.$wamp.call('session.login', [], {
                            username: self.username,
                            password: self.password
                        }).then(function(res) {
                            if (res.success) {
                                self.$store.commit('login', res.user);
                                self.notify("Account Created and Logged In successfully!");
                                self.$cookie.set('session', res.session, 30);
                                self.$router.push('/');
                            } else {
                                self.notify("Error in login after account creation");
                                throw new Error("Error in login after account creation");
                            }
                        });
                    });
                }).catch(() => {
                    self.notify("Please complete all the fields in the form correctly.");
                    return false
                });
            },
            onRecaptchaVerify: function(response) {
                this.recaptcha = response;
            },
            onRecaptchaExpired: function(response) {
                this.notify("Recaptcha expired !", response.error);
            }
        }
    }
</script>
