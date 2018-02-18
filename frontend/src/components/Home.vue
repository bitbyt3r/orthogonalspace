<template>
    <div>
        <h1>Orthogonal Space</h1>
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
                        <md-table-head md-sort-by='factions'>Factions</md-table-head>
                        <md-table-head md-sort-by='players'>Players</md-table-head>
                    </md-table-row>
                </md-table-header>
                <md-table-body>
                    <md-table-row v-for="universe,id in universes" :key="id">
                        <md-table-cell>
                            <router-link :to="'/universe/' + id">
                                <h3>{{ universe.name }}</h3>
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
                    console.log(res);
                    self.universes = res;
                    self.loaded = true;
                }
            });
        }
    }
</script>
