<template>
    <v-container fluid>
        <v-row dense justify="start">
            <v-col v-for="item in items" :key="item.id" style="max-width: 320px;">
                <ItemCard :item="item" :allItems="items" style="margin-top: 10px"/>
            </v-col>
        </v-row>
    </v-container>
</template>


<script>
import ItemCard from '@/components/ItemCard.vue';
import { paths, httpUtils } from '@/utils';

export default {
    name: 'ItemList',
    components: {
        ItemCard,
    },
    data: () => ({
        items: {}
    }),
    methods: {
        async getData() {
            try {
                let res = await fetch(paths.itemList, httpUtils.get())
                this.items = await res.json()
            } catch {
                this.$swal("エラーが発生しました。もう一度お試しください。")
            }
        }
    },
    mounted() {
        this.getData()
        // this.items = [
        //     {
        //         "id": 3,
        //         "image_url": "https://www.sony.jp/products/picture/ILCE-7M3K.jpg",
        //         "is_consumable": true,
        //         "is_lens": false,
        //         "mount_id": 1,
        //         "name": "\u30c7\u30b8\u30bf\u30eb\u4e00\u773c\u30ab\u30e1\u30e9 \u03b17 III",
        //         "release": "Sun, 02 Feb 2020 00:00:00 GMT",
        //         "stock": 1
        //     }
        // ]
    },
}
</script>
