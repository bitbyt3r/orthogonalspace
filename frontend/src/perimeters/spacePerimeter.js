import { createPerimeter } from 'vue-kindergarten';

export default createPerimeter({
    purpose: 'space',

    can: {
        read(space) {
            this.groups.forEach(function(group) {
                if (space.readGroups.includes(group)) {
                    return true;
                }
            });
            return this.isAdmin() || space.readUsers.includes(this.id);
        },
        write(space) {
            this.groups.forEach(function(group) {
                if (space.writeGroups.includes(group)) {
                    return true;
                }
            });
            return this.isAdmin() || space.writeUsers.includes(this.id);
        },
        destroy(space) {
            return this.isAllowed('write', space);
        },
        create() {
            return true;
        }
    },

    isAdmin() {
        return this.child.groups.includes('admin');
    }
});
