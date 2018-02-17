import Vue from 'vue'

Vue.mixin({
    data() {
        return {
          save_open: false
        }
    },
    methods: {
        snackbar: function () {
            return window.vue.$children[0].$refs.snackbar;
        },
        notify: function (message) {
            window.vue.$children[0].$data.message = message;
            window.vue.$children[0].$refs.snackbar.open();
        },
        start_save: function () {
            if (!this.save_open) {
                this.save_open = true;
                window.vue.$children[0].$refs.savebar.open();
            }
        },
        stop_save: function () {
            if (this.save_open) {
                window.vue.$children[0].$refs.savebar.close();
                this.save_open = false;
            }
        }
    }
})
