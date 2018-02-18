<template>
    <div>
        <h1>Create a ship</h1>
        <form>
            <md-input-container required="true" :class="{'md-input-invalid': errors.has('name')}">
                <label>Name</label>
                <md-input name="name" v-model="name" v-validate="'required'"></md-input>
                <span v-show="errors.has('name')">{{ errors.first('name') }}</span>
            </md-input-container>
        </form>
        <md-layout md-row>
            <md-layout md-flex="12" md-align="center">
                <md-button class="md-primary md-raised" :disabled="false" @click="createShip">Create Ship</md-button>
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
                name: "New Ship"
            }
        },
        components: {
        },
        methods: {
            createShip() {
                var self = this;
                this.$validator.validateAll()
                .then((isValidated) => {
                    if(!isValidated) return;
                    this.$wamp.call('ship.create', [], {name: this.name, faction_id: this.$route.params.factionid}).then(function(res) {
                        if (res.success) {
                            self.notify("Created " + self.name + ".");
                            self.$router.push({name: "join"});
                        } else {
                            self.notify("Failed to create the ship: " + res.reason);
                        }
                    });
                }).catch(() => {
                    self.notify("Please name the ship.");
                    return false
                });
            }
        }
    }
</script>
