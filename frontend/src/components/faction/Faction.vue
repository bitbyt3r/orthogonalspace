<template>
    <div>
        <h1>Look at this cool faction:</h1>
        {{ faction.name }}
        <br>It might even have some ships:
        <ul>
             <li v-for="ship in ships">
               {{ ship.name }}
             </li>
        </ul>
    </div>
</template>

<script>
export default {
    data() {
        return {
            faction: {
                name: "UNKNOWN Faction",
                ships: []
            }
        }
    },
    mounted() {
        var self = this;
        this.$wamp.call('faction.get', [this.$route.params.factionid]).then(function(res) {
            if (res.success) {
                self.faction = res.faction;
            } else {
                self.notify("Could not load faction: " + res.reason);
            }
        });
    }
}
</script>
