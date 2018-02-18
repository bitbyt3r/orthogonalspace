<template>
    <div>
        <md-progress v-if="!loaded" style="margin-top: 200px" md-indeterminate></md-progress>
        <md-table-card v-else>
            <md-toolbar>
                <h1 class="md-title">Universes</h1>
                <md-button class="md-icon-button">
                    <md-icon>search</md-icon>
                </md-button>
            </md-toolbar>
            <md-table md-sort='name'>
                <md-table-header>
                    <md-table-row>
                        <md-table-head md-sort-by='name'>Name</md-table-head>
                        <md-table-head md-sort-by='players'>Players</md-table-head>
                        <md-table-head md-sort-by='difficulty'>difficulty</md-table-head>
                    </md-table-row>
                </md-table-header>
                <md-table-body>
                    <md-table-row v-for="universe,name in universes" :key="name">
                        <md-table-cell>
                            <router-link :to="'/universe/' + name + '/play'">
                                <h3>{{ name }}</h3>
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
    </div>
</template>

<script>
    export default {
        name: 'join',
        components: {
        },
        data() {
            return {
                universes: {},
                loaded: false
            };
        },
        methods: {
        },
        mounted: function() {
            var self = this;
            this.$wamp.call('universe.list').then(function(res) {
                if (res) {
                    res.forEach(function(universe) {
                        self.$set(self.universes, universe.name, universe);
                    });
                    self.loaded = true;
                }
            });
        }
    }
</script>
