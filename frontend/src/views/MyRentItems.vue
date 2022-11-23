<template>
    <v-container fluid>
        <v-row dense justify="start" align="start">
            <v-col>
                <RentedItemTable :items="due_items" :title="'レンタル・購入履歴 (未返却)'"/>
                <p>&nbsp;</p>
                <RentedItemTable :items="returnedItems" :title="'レンタル・購入履歴 (返却済)'"/>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import RentedItemTable from '@/components/RentedItemTable.vue';
import { paths, httpUtils } from '@/utils';
export default {
    name: "MyRentItems",
    components: { RentedItemTable },
    data() {
        return {
            returnedItems: [],
            due_items: [],
        };
    },
    methods: {
        async fetchRentedItems() {
            const res = await fetch(paths.myRentedItems, httpUtils.get())
            if (!res.ok) {
                this.$swal({
                    icon: 'error',
                    text: 'エラーが起きたためデータを取得できませんでした'
                })
                return
            }

            const all_items = await res.json()
            this.due_items = all_items['due_items']
            this.returnedItems = all_items['returned_items']
        }
    },
    async mounted() {
        await this.fetchRentedItems()
    }
}
</script>