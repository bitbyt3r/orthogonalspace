import Vue from 'vue'

Vue.mixin({
    methods: {
        log: function() {
            if(this.$config.isLoggingEnabled){
                console.log(args);
            }
        }
    }
})
