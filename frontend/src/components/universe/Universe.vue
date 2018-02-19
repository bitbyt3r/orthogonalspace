<template>
    <div>
        <md-progress v-if="!loaded" style="margin-top: 200px" md-indeterminate></md-progress>
        <div v-else>
            <h1>{{ name }}</h1>
            <md-table-card>
                <md-toolbar>
                    <h1 class="md-title">Factions</h1>
                    <md-button class="md-icon-button">
                        <md-icon>search</md-icon>
                    </md-button>
                </md-toolbar>
                <md-table md-sort='name'>
                    <md-table-header>
                        <md-table-row>
                            <md-table-head md-sort-by='name'>Name</md-table-head>
                            <md-table-head md-sort-by='players'>Players</md-table-head>
                            <md-table-head md-sort-by='somethingelse'>Something Else</md-table-head>
                        </md-table-row>
                    </md-table-header>
                    <md-table-body>
                        <md-table-row v-for="faction,id in factions" :key="id">
                            <md-table-cell>
                                <router-link :to="'/faction/' + id">
                                    <h3>{{ faction.name }}</h3>
                                </router-link>
                            </md-table-cell>
                            <md-table-cell>
                                <p>0</p>
                            </md-table-cell>
                            <md-table-cell>
                                <p>3</p>
                            </md-table-cell>
                        </md-table-row>
                    </md-table-body>
                </md-table>
            </md-table-card>
            <router-link tag="md-button" :to="'/universe/' + $route.params.universeid + '/faction/create'" class="md-fab md-fab-bottom-right">
                <md-icon>add</md-icon>
            </router-link>
        </div>
    </div>
</template>

<script>
    export default {
        components: {
        },
        data() {
            return {
                factions: {},
                loaded: false,
                name: ""
            };
        },
        methods: {
        },
        mounted: function() {
            var self = this;
            this.$wamp.call('universe.list_factions', [this.$route.params.universeid]).then(function(res) {
                if (res) {
                    console.log(res);
                    self.factions = res.factions;
                    self.loaded = true;
                }
            });
            this.$wamp.call('universe.get', [this.$route.params.universeid]).then(function(res) {
                self.name = res.universe.name;
            });
        }
    }
</script>
