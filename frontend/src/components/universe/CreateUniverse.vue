<template>
    <div>
        <h1>Create The Universe</h1>
        <form>
            <md-input-container required="true" :class="{'md-input-invalid': errors.has('name')}">
                <label>Name</label>
                <md-input name="name" v-model="name" v-validate="'required'"></md-input>
                <span v-show="errors.has('name')">{{ errors.first('name') }}</span>
            </md-input-container>
        </form>
        <md-layout md-row>
            <md-layout md-flex="12" md-align="center">
                <md-button class="md-primary md-raised" :disabled="false" @click="createUniverse">Create Universe</md-button>
            </md-layout>
        </md-layout>
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
        name: 'create',
        data() {
            return {
                name: "New Universe"
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
            createUniverse() {
                var self = this;
                this.$validator.validateAll()
                .then((isValidated) => {
                    if(!isValidated) return;
                    this.$wamp.call('universe.create', [], {name: this.name, parameters: {}}).then(function(res) {
                        if (res.success) {
                            self.notify("BANG! Created " + self.name + ".");
                            self.$router.push({name: "universe", params: {id: res.id}});
                        } else {
                            self.notify("Failed to create the universe: " + res.reason);
                        }
                    });
                }).catch(() => {
                    self.notify("Please name the universe.");
                    return false
                });
            }
        }
    }
</script>
