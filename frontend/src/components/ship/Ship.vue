<template>
    <div>
        {{ ship.name }} is underway. Click here to join the crew:
        <md-button class="md-primary md-raised" :disabled="false" @click="enlist">Enlist</md-button>
    </div>
</template>

<style>
a-scene {
  height: 300px;
  width: 600px;
}
</style>

<script>
import _ from 'lodash';

export default {
    computed: {
        ship() {
            return _.cloneDeep(this.$store.state.ship.ship);
        }
    },
    methods: {
        enlist() {
            this.$router.push('/play/' + this.$route.params.shipid);
        },
    },
    mounted() {
        var self = this;
        this.$wamp.call('ship.get', [this.$route.params.shipid]).then(function(res) {
            if (res.success) {
                self.$store.commit('load_ship', res.ship);
            } else {
                self.notify("Could not load ship: " + res.reason);
            }
        });
    }
}
</script>
