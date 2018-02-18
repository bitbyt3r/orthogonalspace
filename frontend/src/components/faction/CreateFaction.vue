<template>
    <div>
        <h1>Create a faction</h1>
        <form>
            <md-input-container required="true" :class="{'md-input-invalid': errors.has('name')}">
                <label>Name</label>
                <md-input name="name" v-model="name" v-validate="'required'"></md-input>
                <span v-show="errors.has('name')">{{ errors.first('name') }}</span>
            </md-input-container>
        </form>
        <md-layout md-row>
            <md-layout md-flex="12" md-align="center">
                <md-button class="md-primary md-raised" :disabled="false" @click="createFaction">Create Faction</md-button>
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
                name: "New Faction"
            }
        },
        components: {
        },
        methods: {
            createFaction() {
                var self = this;
                this.$validator.validateAll()
                .then((isValidated) => {
                    if(!isValidated) return;
                    this.$wamp.call('faction.create', [], {name: this.name, parameters: {}, universe: this.$route.params.universeid}).then(function(res) {
                        if (res.success) {
                            self.notify("Created " + self.name + ".");
                            self.$router.push({name: "join"});
                        } else {
                            self.notify("Failed to create the faction: " + res.reason);
                        }
                    });
                }).catch(() => {
                    self.notify("Please name the faction.");
                    return false
                });
            }
        }
    }
</script>
