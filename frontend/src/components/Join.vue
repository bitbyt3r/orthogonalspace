<template>
    <div>
        <h1>Universes</h1>
        <md-list v-if="universes">
            <md-list-item v-for="universe,name in universes" :key="name">{{ name }}</md-list-item>
        </md-list>
        <p v-else>No known universes exist.</p>
    </div>
</template>

<script>
    export default {
        name: 'join',
        components: {
        },
        data() {
            return {
                universes: {}
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
                }
            });
        }
    }
</script>
