<template>
    <div>
        <div v-if="ship.launched">
            {{ ship.name }} is underway. Click here to join the crew:
            <md-button class="md-primary md-raised" :disabled="false" @click="enlist">Enlist</md-button>
        </div>
        <div v-else>
            <h1>Customize Your Ship</h1>
            <md-layout md-row>
                <md-layout md-flex-small="100">
                    <form>
                        <md-input-container required="true" :class="{'md-input-invalid': errors.has('name')}">
                            <label>Name</label>
                            <md-input @change="update" name="name" v-model="ship.name" v-validate="'required'"></md-input>
                            <span v-show="errors.has('name')">{{ errors.first('name') }}</span>
                        </md-input-container>
                        <md-input-container>
                            <label for="shiptype">Ship Type</label>
                            <md-select @change="update" name="shiptype" id="shiptype" v-model="ship.type">
                              <md-option v-for="shiptype in $store.state.ship.shiptypes" :key="shiptype.id" :value="shiptype.id">{{ shiptype.name }}</md-option>
                            </md-select>
                        </md-input-container>
                        <md-checkbox @change="update" id="ready" name="ready" v-model="ready">Ready</md-checkbox>
                    </form>
                </md-layout>
                <md-layout md-flex-small="100" md-hide-xsmall>
                    <a-scene debug embedded>
                        <a-assets>
                        </a-assets>
                        <a-entity id="camera" ref="camera" position="0 1 0" camera></a-entity>
                        <a-text position="0 2.5 -3" align="center" color="#000000" scale="2 2 2" id="shipname"></a-text>
                        <a-entity position="0 0 -3">
                            <a-animation attribute="rotation" easing="linear" dur="3000" to="0 360 0" repeat="indefinite"></a-animation>
                            <a-box position="-1 0.5 0" rotation="0 45 0" color="#4CC3D9" shadow></a-box>
                            <a-sphere position="0 1.25 -2" radius="1.25" color="#EF2D5E" shadow></a-sphere>
                            <a-cylinder position="1 0.75 0" radius="0.5" height="1.5" color="#FFC65D" shadow></a-cylinder>
                            <a-plane position="0 0 -1" rotation="-90 0 0" width="4" height="4" color="#7BC8A4" shadow></a-plane>
                        </a-entity>
                        <a-sky color="#FFFFFF"></a-sky>
                        </a-scene>
                    <p>{{ description }}</p>
                </md-layout>
            </md-layout>
        </div>
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
    data() {
        return {
            ready: false
        }
    },
    computed: {
        description() {
            if (this.$store.state.ship.shiptypes.hasOwnProperty(this.ship.type)) {
                return this.$store.state.ship.shiptypes[this.ship.type].description;
            }
            return "Select a ship type to get a description";
        },
        ship() {
            return _.cloneDeep(this.$store.state.ship.ship);
        }
    },
    methods: {
        update() {
            var self = this;
            this.$nextTick(function() {
                self.$store.commit('update_ship', {"name": self.ship.name, "type": self.ship.type})
                self.$store.commit('update_ready', self.ready);
                var text = document.getElementById('shipname');
                text.setAttribute("value", self.ship.name);
                self.$wamp.call('ship.update_parameters', [], {ship_id: self.ship.id, parameters: {type: self.ship.type, name: self.ship.name}});
            });
        }
    },
    mounted() {
        var self = this;
        this.$wamp.call('ship.get', [this.$route.params.shipid]).then(function(res) {
            console.log(res);
            if (res.success) {
                self.$store.commit('load_ship', res.ship);
                self.update();
            } else {
                self.notify("Could not load ship: " + res.reason);
            }
        });
        this.$wamp.call('ship.list_types').then(function(res) {
            if (res.success) {
                self.$store.commit('load_shiptypes', res.types);
            }
        });
    }
}
</script>
