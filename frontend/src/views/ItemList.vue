<template>
    <v-app>
        <div>
            <v-container>
                <v-row>
                    <v-col cols="4" v-for="item in items" :key="item.id">
                        <ItemCard :title="item.name" :imageUrl="item.image_url" :itemId="item.id" />
                    </v-col>
                </v-row>
            </v-container>
        </div>
    </v-app>
</template>


<script>
import ItemCard from '@/components/ItemCard.vue';
import { envs, httpUtils } from '@/utils';

export default {
    name: 'ItemList',
    components: {
        ItemCard
    },
    data: () => ({
        items: null
    }),
    methods: {
        async getData() {
            try{
                let res = await fetch(envs.baseURL + '/items', httpUtils.get())
                this.items = await res.json()
            } catch {
                this.$swal("エラーが起きました。もう一度最初からお試しください。")
            }
        }
    },
    mounted() {
        this.getData()
    },
}
</script>
