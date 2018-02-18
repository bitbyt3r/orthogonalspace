<template>
    <div>
        <md-progress v-if="!loaded" style="margin-top: 200px" md-indeterminate></md-progress>
        <md-table-card v-else>
            <md-toolbar>
                <h1 class="md-title">Ships</h1>
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
                    <md-table-row v-for="ship,id in ships" :key="id">
                        <md-table-cell>
                            <router-link :to="'ship/' + id">
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
            this.$wamp.call('ships.list', [], {universe: this.$route.params.universeid, faction: this.$route.params.factionid}).then(function(res) {
                if (res) {
                    self.ships = res;
                    self.loaded = true;
                }
            });
        }
    }
</script>
