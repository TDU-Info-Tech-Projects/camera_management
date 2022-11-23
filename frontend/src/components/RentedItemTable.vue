<template>
    <v-data-table :headers="headers" :items="items" sort-by="due_date" class="elevation-1">
        <template v-slot:top>
            <v-toolbar color="primary">
                <v-toolbar-title style="color: white">{{                                                                                                                                                                                                                                                                                                                                                         title                                                                                                                                                                                                                                                                                                                                                         }}</v-toolbar-title>

                <v-dialog v-model="dialog" max-width="500px">
                    <v-card>
                        <v-card-title class="text-h5">{{ selectedItem ? selectedItem.Item.name : '' }}を返却しますか
                        </v-card-title>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn elevation="1" color="warning" @click="close">
                                キャンセル
                            </v-btn>
                            <v-btn elevation="1" color="primary" @click="returnConfirm">
                                返却
                            </v-btn>
                            <v-spacer></v-spacer>
                        </v-card-actions>
                    </v-card>
                </v-dialog>

            </v-toolbar>
        </template>

        <template v-slot:item.RentItem.loan_date="{ item }">
            {{                                                                                                                                                                                                                                                                                                                                                         new Date(item.RentItem.loan_date).toISOString().slice(0, 10)                                                                                                                                                                                                                                                                                                                                                         }}
        </template>

        <template v-slot:item.RentItem.due_date="{ item }">
            {{                                                                                                                                                                                                                                                                                                                                                         item.RentItem.due_date && new Date(item.RentItem.due_date).toISOString().slice(0, 10)                                                                                                                                                                                                                                                                                                                                                         }}
        </template>

        <template v-slot:item.RentItem.return_date="{ item }">
            {{                                                                                                                                                                                                                                                                                                                                                         item.RentItem.return_date ? new Date(item.RentItem.return_date).toISOString().slice(0, 10) : '-'                                                                                                                                                                                                                                                                                                                                                         }}
        </template>

        <template v-slot:item.actions="{ item }">
            <v-btn elevation="1" color="primary" depressed @click="returnItem(item)" v-if="isReturnButtonVisible(item)">
                返却
            </v-btn>
            <span>&nbsp;</span>
        </template>
    </v-data-table>
</template>
  
<script>
import { store } from '@/store'
import { httpUtils, paths } from '@/utils'
export default {
    props: {
        items: Array,
        title: String
    },
    data: () => ({
        dialog: false,
        selectedItem: null,
        headers: [
            {
                text: '商品名',
                sortable: false,
                value: 'Item.name'
            },
            {
                text: '予約日',
                sortable: true,
                value: 'RentItem.loan_date'
            },
            {
                text: '返却予定日',
                sortable: true,
                value: 'RentItem.due_date'
            },
            {
                text: '返却日',
                sortable: true,
                value: 'RentItem.return_date'
            },
            { text: '', value: 'actions', sortable: false },
        ],
    }),

    computed: {
        isAdmin() {
            return store.user.is_admin
        }
    },

    watch: {
        dialog(val) {
            val || this.close()
        },
    },

    methods: {
        returnItem(item) {
            this.selectedItem = item
            this.dialog = true
        },

        async returnConfirm() {
            this.close()

            const res = await fetch(paths.returnItem, httpUtils.post({
                ids: [this.selectedItem.RentItem.id]
            }))

            if (!res.ok) {
                this.$swal({
                    icon: 'error',
                    text: 'エラー発生しました。もう一度お試しください。'
                })
                return
            }

            this.$swal({
                icon: 'success',
                text: '正常に処理しました。ご返却ありがとうございます。'
            }).then(() => {
                location.reload()
            })
        },

        close() {
            this.dialog = false
        },

        isReturnButtonVisible(item) {
            return !item.Item.is_consumable && !item.RentItem.return_date
        }
    },
}
</script>
  