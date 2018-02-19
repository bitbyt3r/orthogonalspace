<template>
    <div>
        <md-progress v-if="!loaded" style="margin-top: 200px" md-indeterminate></md-progress>
        <div>
            <md-table-card>
                <md-toolbar>
                    <h1 class="md-title">Preparing to Launch</h1>
                    <md-button class="md-icon-button">
                        <md-icon>search</md-icon>
                    </md-button>
                </md-toolbar>
                <md-table md-sort='name'>
                    <md-table-header>
                        <md-table-row>
                            <md-table-head md-sort-by='name'>Name</md-table-head>
                            <md-table-head md-sort-by='players'>Players</md-table-head>
                        </md-table-row>
                    </md-table-header>
                    <md-table-body>
                        <md-table-row v-for="ship,id in ships" v-if="!ship.launched" :key="id">
                            <md-table-cell>
                                <router-link :to="'/ship/' + id">
                                    <h3>{{ ship.name }}</h3>
                                </router-link>
                            </md-table-cell>
                            <md-table-cell>
                                <p>5</p>
                            </md-table-cell>
                        </md-table-row>
                    </md-table-body>
                </md-table>
            </md-table-card>
            <br>
            <md-table-card>
                <md-toolbar>
                    <h1 class="md-title">Underway</h1>
                    <md-button class="md-icon-button">
                        <md-icon>search</md-icon>
                    </md-button>
                </md-toolbar>
                <md-table md-sort='name'>
                    <md-table-header>
                        <md-table-row>
                            <md-table-head md-sort-by='name'>Name</md-table-head>
                            <md-table-head md-sort-by='guns'>Guns</md-table-head>
                            <md-table-head md-sort-by='books'>Books</md-table-head>
                        </md-table-row>
                    </md-table-header>
                    <md-table-body>
                        <md-table-row v-for="ship,id in ships" v-if="ship.launched" :key="id">
                            <md-table-cell>
                                <router-link :to="'/ship/' + id">
                                    <h3>{{ ship.name }}</h3>
                                </router-link>
                            </md-table-cell>
                            <md-table-cell>
                                <p>many</p>
                            </md-table-cell>
                            <md-table-cell>
                                <p>few</p>
                            </md-table-cell>
                        </md-table-row>
                    </md-table-body>
                </md-table>
            </md-table-card>
        </div>
        <router-link tag="md-button" :to="'/faction/' + $route.params.factionid + '/ship/create'" class="md-fab md-fab-bottom-right">
            <md-icon>add</md-icon>
        </router-link>
    </div>
</template>

<script>
    export default {
        name: 'join',
        components: {
        },
        data() {
            return {
                ships: {},
                loaded: false
            };
        },
        methods: {
        },
        mounted: function() {
            var self = this;
            this.$wamp.call('faction.list_ships', [this.$route.params.factionid]).then(function(res) {
                if (res) {
                    self.ships = res.ships;
                    self.loaded = true;
                }
            });
        }
    }
</script>
