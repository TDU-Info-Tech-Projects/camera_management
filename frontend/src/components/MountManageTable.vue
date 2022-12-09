<template>
    <v-data-table :headers="headers" :items="mounts" class="elevation-1">
        <template v-slot:top>
            <v-toolbar color="primary" style="color: white;">
                <v-toolbar-title>マウント一覧</v-toolbar-title>
                <v-spacer></v-spacer>
                <v-dialog v-model="dialog" max-width="500px">
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn elevation="3" class="mb-2" v-bind="attrs" v-on="on">
                            マウント追加
                        </v-btn>
                    </template>
                    <v-card>
                        <v-card-title>
                            <span class="text-h5">{{ formTitle }}</span>
                        </v-card-title>

                        <v-card-text>
                            <v-container>
                                <v-text-field v-model="editedItem.id" label="マウントID" disabled v-if="isEditMode" />
                                <v-text-field v-model="editedItem.name" label="マウント名" />
                            </v-container>
                        </v-card-text>

                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="blue darken-1" text @click="close" :disabled="loading">
                                キャンセル
                            </v-btn>
                            <v-btn color="blue darken-1" text @click="save" :disabled="loading">
                                保存
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
                <v-dialog v-model="dialogDelete" max-width="500px">
                    <v-card>
                        <v-card-title class="text-h5">「{{ editedItem.name }}」を削除しますか。</v-card-title>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="blue darken-1" text @click="closeDelete">キャンセル</v-btn>
                            <v-btn color="blue darken-1" text @click="deleteItemConfirm">削除</v-btn>
                            <v-spacer></v-spacer>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </v-toolbar>
        </template>
        <template v-slot:item.actions="{ item }">
            <v-icon small class="mr-2" @click="editItem(item)">
                mdi-pencil
            </v-icon>
            <v-icon small @click="deleteItem(item)">
                mdi-delete
            </v-icon>
        </template>
    </v-data-table>
</template>
  
<script>
import { httpUtils, paths } from '@/utils'

export default {
    name: 'MountManageTable',
    props: {
        mountsData: Array
    },
    data: () => ({
        dialog: false,
        dialogDelete: false,
        isEditMode: false,
        loading: false,
        headers: [
            {
                text: 'ID',
                align: 'start',
                sortable: false,
                value: 'id',
            },
            {
                text: 'マウント名',
                align: 'start',
                sortable: false,
                value: 'name',
            },
            { text: '編集・削除', value: 'actions', sortable: false },
        ],
        editedItem: {
            id: "",
            name: "",
        },
        defaultItem: {
            id: "",
            name: "",
        },
    }),

    computed: {
        formTitle() {
            return this.isEditMode ? 'マウント編集' : 'マウント追加'
        },
        mounts() {
            return this.$props.mountsData
        }
    },

    watch: {
        dialog(val) {
            val || this.close()
        },
        dialogDelete(val) {
            val || this.closeDelete()
        },
    },

    methods: {
        editItem(item) {
            this.isEditMode = true
            this.editedItem = Object.assign({}, item)
            this.dialog = true
        },

        deleteItem(item) {
            this.editedItem = Object.assign({}, item)
            this.dialogDelete = true
        },

        async deleteItemConfirm() {
            this.closeDelete()
            const res = await fetch(paths.deleteMount, httpUtils.post({
                id: this.editedItem.id
            }))

            if (!res.ok) {
                this.$swal({
                    icon: 'error',
                    text: 'エラーが発生しました。もう一度お試しください。'
                })
                return
            }

            location.reload()
        },

        close() {
            this.dialog = false
            this.isEditMode = false
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
            })
        },

        closeDelete() {
            this.dialogDelete = false
        },

        async save() {
            this.loading = true
            const res = await fetch(paths.addMount, httpUtils.post(this.editedItem))
            this.loading = false

            if (!res.ok) {
                this.$swal({
                    icon: 'error',
                    text: 'エラーが発生しました。入力内容を確認してからもう一度お試しください。'
                })
                return
            }

            this.close()
            location.reload()
        },
    },
}
</script>
  