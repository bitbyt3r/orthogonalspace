<template>
    <div>
        <h1>Customize Your Ship</h1>
        <md-layout md-row>
            <md-layout md-flex-small="100">
                <form>
                    <md-input-container required="true" :class="{'md-input-invalid': errors.has('name')}">
                        <label>Name</label>
                        <md-input @change="update" :disabled="ready" name="name" v-model="ship.name" v-validate="'required'"></md-input>
                        <span v-show="errors.has('name')">{{ errors.first('name') }}</span>
                    </md-input-container>
                    <md-input-container>
                        <label for="shiptype">Ship Type</label>
                        <md-select @change="update" :disabled="ready" name="shiptype" id="shiptype" v-model="ship.type">
                          <md-option v-for="(shiptype, id) in $store.state.ship.shiptypes" :key="id" :value="id">{{ shiptype.name }}</md-option>
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
                    <a-entity position="0 1 -3">
                        <a-animation attribute="rotation" easing="linear" dur="3000" to="0 360 0" repeat="indefinite"></a-animation>
                        <a-entity position="0 0 0" rotation="0 0 0" material="color: blue" id="shipmodel"></a-entity>
                    </a-entity>
                    <a-sky color="#FFFFFF"></a-sky>
                    </a-scene>
                <p>{{ description }}</p>
            </md-layout>
        </md-layout>
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
            ready: false,
            current_sub: null
        }
    },
    computed: {
        description() {
            if (this.$store.state.ship.shiptypes.hasOwnProperty(this.ship.type)) {
                return this.$store.state.ship.shiptypes[this.ship.type].description;
            }
            return "Select a ship type to get a description";
        },
        geometry() {
            if (this.$store.state.ship.shiptypes.hasOwnProperty(this.ship.type)) {
                return this.$store.state.ship.shiptypes[this.ship.type].geometry;
            }
            return "box";
        },
        ship() {
            return _.cloneDeep(this.$store.state.ship.ship);
        }
    },
    methods: {
        allReady() {
            if (!this.ready) {
                console.log("Told to enter game when I am not ready!");
            }
            this.notify("Starting Game...");
            this.enlist();
        },
        enlist() {
            this.$router.push('/play/' + this.$route.params.shipid);
        },
        update() {
            var self = this;
            this.$nextTick(function() {
                console.log(self.$store.state.ship);
                self.$store.commit('update_ship', {"name": self.ship.name, "type": self.ship.type})
                self.$store.commit('update_ready', self.ready);
                var text = document.getElementById('shipname');
                text.setAttribute("value", self.ship.name);
                var model = document.getElementById('shipmodel');
                model.setAttribute("geometry", "primitive", self.geometry);
                self.$wamp.call('ship.set_name', [self.ship.id, self.ship.name]);
                self.$wamp.call('ship.set_type', [self.ship.id, self.ship.type]);

                if (self.ready) {
                    if (self.current_sub) {
                        self.$wamp.unsubscribe(self.current_sub).then(function(sub) {
                            self.current_sub = null;
                            self.$wamp.call('wamp.subscription.lookup', ['ship.readynotice.' + self.$route.params.shipid]).then(function(res) {
                                if (res) {
                                    self.$wamp.call('wamp.subscription.count_subscribers', [res]).then(function(num_users) {
                                        if (!num_users) {
                                            self.$wamp.call('ship.launch', [self.ship.id]);
                                            self.$wamp.publish('ship.ready.' + self.$route.params.shipid, [], {}, {exclude_me: false});
                                        } else {
                                            console.log("Still waiting on " + num_users + " people.");
                                        }
                                    });
                                } else {
                                    console.log("Ship is ready! (2)");
                                    self.$wamp.call('ship.launch', [self.ship.id]);
                                    self.$wamp.publish('ship.ready.' + self.$route.params.shipid, [], {}, {exclude_me: false});
                                }
                            });
                        });
                    }
                } else {
                    if (!self.current_sub) {
                        self.$wamp.subscribe('ship.ready.' + self.$route.params.shipid, console.log).then(function(sub) {
                            self.current_sub = sub;
                        });
                    }
                }
            });
        }
    },
    mounted() {
        var self = this;
        this.$wamp.subscribe('ship.readynotice.' + this.$route.params.shipid, console.log).then(function(sub) {
            self.current_sub = sub;
        });
        this.$wamp.subscribe('ship.ready.' + this.$route.params.shipid, this.allReady);
        this.$wamp.call('shipconfig.get', [this.$route.params.shipid]).then(function(res) {
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
