<template>
    <div>
        <h1>Look at this cool ship:</h1>
        {{ ship.name }}
    </div>
</template>

<script>
export default {
    data() {
        return {
            ship: {
                name: "UNKNOWN Ship"
            }
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
    }
}
</script>
