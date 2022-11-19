<template>
    <v-app>
        <div>
            <v-container>
                <v-row>
                    <v-col cols="4">
                        <ItemCard :title="'Camera'" :imageUrl="'ggg'" :itemId="'jffdfd'" />
                    </v-col>
                </v-row>
            </v-container>
        </div>
    </v-app>
</template>


<script>
import ItemCard from '@/components/ItemCard.vue';

export default {
    name: 'HomeView',
    components: {
        ItemCard
    }
}
</script>
