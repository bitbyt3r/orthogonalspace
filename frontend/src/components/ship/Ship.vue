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
                            <md-input name="name" v-model="ship.name" v-validate="'required'"></md-input>
                            <span v-show="errors.has('name')">{{ errors.first('name') }}</span>
                        </md-input-container>
                        <md-input-container>
                            <label for="shiptype">Ship Type</label>
                            <md-select name="shiptype" id="shiptype" v-model="ship.type">
                              <md-option v-for="(type, id) in shiptypes" :key="id" :value="id">{{ type.name }}</md-option>
                            </md-select>
                        </md-input-container>
                        <md-input-container>
                            <md-checkbox id="ready" name="ready" v-model="ready">Ready</md-checkbox>
                        </md-input-container>
                    </form>
                </md-layout>
                <md-layout md-flex-small="100" md-hide-xsmall>
                    <div style="height: 300px; width: 300px">
                        <a-scene debug embedded ref="scene">
                            <a-assets>
                            </a-assets>
                            <a-entity id="camera" look-controls wasd-controls ref="camera" position="0 1 0" camera></a-entity>
                            <a-box position="-1 0.5 -3" rotation="0 45 0" color="#4CC3D9" shadow></a-box>
                            <a-text position="0 2.5 -3" align="center" color="#000000" scale="2 2 2" :value="ship.name"></a-text>
                            <a-sphere position="0 1.25 -5" radius="1.25" color="#EF2D5E" shadow></a-sphere>
                            <a-cylinder position="1 0.75 -3" radius="0.5" height="1.5" color="#FFC65D" shadow></a-cylinder>
                            <a-plane position="0 0 -4" rotation="-90 0 0" width="4" height="4" color="#7BC8A4" shadow></a-plane>
                            <a-sky color="#ECECEC"></a-sky>
                        </a-scene>
                    </div>
                    <p>{{ description }}</p>
                </md-layout>
            </md-layout>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            ship: {
                name: "UNKNOWN Ship",
                type: ""
            },
            ready: false,
            shiptypes: {}
        }
    },
    computed: {
        description() {
            if (this.ship.type) {
                return this.shiptypes[this.ship.type].description;
            }
            return "Select a ship type to see a description";
        }
    },
    mounted() {
        var self = this;
        this.$wamp.call('ship.get', [this.$route.params.shipid]).then(function(res) {
            if (res.success) {
                self.ship = res.ship;
            } else {
                self.notify("Could not load ship: " + res.reason);
            }
        });
        this.$wamp.call('ship.list_types').then(function(res) {
            if (res.success) {
                console.log(res);
                self.shiptypes = res.types;
            }
        });
    }
}
</script>
