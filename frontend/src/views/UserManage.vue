<template>
    <v-container fluid>
        <v-row dense justify="start" align="start">
            <v-col>
                <UserManageTable :usersData="users" />
            </v-col>
        </v-row>
    </v-container>
</template>


<script>
import UserManageTable from '@/components/UserManageTable.vue';
import { paths, httpUtils } from '@/utils';
export default {
    name: "ProductManage",
    components: { UserManageTable },
    data() {
        return {
            users: [],
        };
    },
    methods: {
        async fetchUsers() {
            const res = await fetch(paths.adminUserList, httpUtils.get())
            if (!res.ok) {
                this.$swal({
                    icon: 'error',
                    text: 'エラーが起きたためデータを取得できませんでした'
                })
                return
            }

            this.users = await res.json()
        }
    },
    async mounted() {
        await this.fetchUsers()
    }
}
</script>