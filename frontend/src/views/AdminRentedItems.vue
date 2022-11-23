<template>
    <v-container fluid>
        <v-row dense justify="start" align="start">
            <v-col>
                <RentedItemTable :items="overdue_items" :title="'レンタル・購入履歴 (返却日超過！)'" color="red" v-if="overdue_items.length"/>
                <p />
                <RentedItemTable :items="due_items" :title="'レンタル・購入履歴 (未返却)'" color="primary"/>
                <p />
                <RentedItemTable :items="returnedItems" :title="'レンタル・購入履歴 (返却済)'" color="primary"/>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import RentedItemTable from '@/components/RentedItemTable.vue';
import { paths, httpUtils } from '@/utils';
export default {
    name: "AdminRentedItems",
    components: { RentedItemTable },
    data() {
        return {
            returnedItems: [],
            due_items: [],
            overdue_items: []
        };
    },
    methods: {
        async fetchRentedItems() {
            const res = await fetch(paths.adminRentedItems, httpUtils.get())
            const overdueRes = await fetch(paths.adminOverdueRentedItems, httpUtils.get())
            if (!res.ok || !overdueRes.ok) {
                this.$swal({
                    icon: 'error',
                    text: 'エラーが起きたためデータを取得できませんでした'
                })
                return
            }

            const all_items = await res.json()
            this.due_items = all_items['due_items']
            this.returnedItems = all_items['returned_items']
            this.overdue_items = await overdueRes.json()
        }
    },
    async mounted() {
        await this.fetchRentedItems()
    }
}
</script>