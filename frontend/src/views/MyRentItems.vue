<template>
    <v-container fluid>
        <v-row dense justify="start" align="start">
            <v-col>
                <RentedItemTable :items="rentedItems"/>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import RentedItemTable from '@/components/RentedItemTable.vue';
import { envs, httpUtils } from '@/utils';
export default {
    name: "MyRentItems",
    components: { RentedItemTable },
    data() {
        return {
            rentedItems: []
        };
    },
    methods: {
        async fetchRentedItems() {
            const res = await fetch(envs.baseURL + '/items/rented', httpUtils.get())
            if (!res.ok) {
                this.$swal({
                    icon: 'error',
                    text: 'エラーが起きたためデータを取得できませんでした'
                })
                return
            }

            this.rentedItems = await res.json()
        }
    },
    async mounted() {
        await this.fetchRentedItems()
    }
}
</script>