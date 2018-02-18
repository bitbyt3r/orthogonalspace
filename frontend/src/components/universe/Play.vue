<template>
    <div>
        <h1>This is where you play the game.</h1>
        <div style="height: 500px; width: 500px">
            <a-scene debug embedded ref="scene">
                <a-assets>
                </a-assets>
                <a-entity id="camera" look-controls wasd-controls ref="camera" position="0 1 0" camera></a-entity>
                <a-box position="-1 0.5 -3" rotation="0 45 0" color="#4CC3D9" shadow></a-box>
                <a-text position="0 2.5 -3" align="center" color="#000000" scale="2 2 2" :value="universe.name"></a-text>
                <a-sphere position="0 1.25 -5" radius="1.25" color="#EF2D5E" shadow></a-sphere>
                <a-cylinder position="1 0.75 -3" radius="0.5" height="1.5" color="#FFC65D" shadow></a-cylinder>
                <a-plane position="0 0 -4" rotation="-90 0 0" width="4" height="4" color="#7BC8A4" shadow></a-plane>
                <a-sky color="#ECECEC"></a-sky>
            </a-scene>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            universe: {
                name: "UNKNOWN"
            }
        }
    },
    mounted() {
        var self = this;
        this.$wamp.call('universe.get', [this.$route.params.id]).then(function(res) {
            self.universe = res;
        });
    }
}
</script>
