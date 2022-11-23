<template>
    <v-container fluid>
        <v-row dense justify="start" align="start">
            <v-col>
                <MountManageTable :mountsData="mounts" />
                <p />
                <ProductManageTable :productsData="products" :mountsData="mounts"/>
            </v-col>
        </v-row>
    </v-container>
</template>


<script>
import ProductManageTable from '@/components/ProductManageTable.vue';
import MountManageTable from '@/components/MountManageTable.vue';
import { paths, httpUtils } from '@/utils';
export default {
    name: "ProductManage",
    components: { ProductManageTable, MountManageTable },
    data() {
        return {
            products: [],
            mounts: []
        };
    },
    methods: {
        async fetchRentedItems() {
            const res = await fetch(paths.itemList, httpUtils.get())
            const mountRes = await fetch(paths.mountList, httpUtils.get())
            if (!res.ok || !mountRes.ok) {
                this.$swal({
                    icon: 'error',
                    text: 'エラーが起きたためデータを取得できませんでした'
                })
                return
            }

            this.products = await res.json()
            this.mounts = await mountRes.json()
        }
    },
    async mounted() {
        await this.fetchRentedItems()
    }
}
</script>