<template>
    <v-app>
        <div>
            <v-container>
                <v-row>
                    <v-col v-for="n in 24" :key="n" cols="4">
                            <router-link :to="{ path: '/about',query:{user_id:n}}">
                                <v-avatar color="grey lighten-2" size="128"></v-avatar>
                            </router-link>
                    </v-col>
                </v-row>
            </v-container>
        </div>
    </v-app>
</template>


<script>
export default {
    name: 'HomeView',
    components: {
        
    }
}
</script>
