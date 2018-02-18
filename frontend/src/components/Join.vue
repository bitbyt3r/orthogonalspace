<template>
    <div>
        <h1>Universes</h1>
        <md-list v-if="universes.length">
            <md-list-item v-for="universe in universes" :key="universe.name"></md-list-item>
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
                universes: []
            };
        },
        methods: {
        },
        mounted: function() {
            var self = this;
            this.$wamp.call('universe.list').then(function(res) {
                console.log(res);
                if (res) {
                    self.universes = res;
                }
            });
        }
    }
</script>
