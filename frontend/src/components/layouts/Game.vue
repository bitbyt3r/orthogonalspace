<template>
    <div>
        <md-layout md-gutter id="main-content" md-align="center">
            <md-layout md-column md-flex-xsmall="100" md-flex-small="100" md-flex-medium="80" md-flex-large="66" md-flex-xlarge="50">
                <router-view></router-view>
            </md-layout>
        </md-layout>
    </div>
</template>

<script>
export default {
}
</script>
