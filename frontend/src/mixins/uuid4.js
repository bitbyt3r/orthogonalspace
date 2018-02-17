import Vue from 'vue'

var get_uuid4 = function() {
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
        }

Vue.mixin({
    methods: {
        get_uuid4: get_uuid4
    }
});

export default {
    get_uuid4
};
