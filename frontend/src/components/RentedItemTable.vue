<template>
    <v-data-table :headers="headers" :items="items" sort-by="calories" class="elevation-1">
        <template v-slot:top>
            <v-toolbar  color="primary">
                <v-toolbar-title style="color: white">レンタル・購入履歴</v-toolbar-title>

                <v-dialog v-model="dialog" max-width="500px">
                    <v-card>
                        <v-card-title class="text-h5">Are you sure you want to delete this item?</v-card-title>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
                            <v-btn color="blue darken-1" text @click="save">OK</v-btn>
                            <v-spacer></v-spacer>
                        </v-card-actions>
                    </v-card>
                </v-dialog>

                <v-dialog v-model="dialogDelete" max-width="500px">
                    <v-card>
                        <v-card-title class="text-h5">Are you sure you want to delete this item?</v-card-title>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
                            <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
                            <v-spacer></v-spacer>
                        </v-card-actions>
                    </v-card>
                </v-dialog>

            </v-toolbar>
        </template>
        <template v-slot:item.actions="{ item }">
            <v-btn elevation="1" color="primary" depressed @click="editItem(item)">
                返却
            </v-btn>
            <span>&nbsp;</span>
            <v-btn elevation="1" color="error" depressed @click="deleteItem(item)">
                削除
            </v-btn>
        </template>
    </v-data-table>
</template>
  
<script>
export default {
    props: {
        items: Array
    },
    data: () => ({
        dialog: false,
        dialogDelete: false,
        headers: [
            {
                text: '商品名',
                sortable: false,
                value: 'name'
            },
            { text: '', value: 'actions', sortable: false },
        ],
        desserts: [],
        editedIndex: -1,
        editedItem: {
            name: '',
            calories: 0,
            fat: 0,
            carbs: 0,
            protein: 0,
        },
        defaultItem: {
            name: '',
            calories: 0,
            fat: 0,
            carbs: 0,
            protein: 0,
        },
    }),

    computed: {
        formTitle() {
            return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
        },
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
            this.editedIndex = this.desserts.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialog = true
        },

        deleteItem(item) {
            this.editedIndex = this.desserts.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialogDelete = true
        },

        deleteItemConfirm() {
            this.closeDelete()
        },

        close() {
            this.dialog = false
        },

        closeDelete() {
            this.dialogDelete = false
        },

        save() {
            this.close()
        },
    },
}
</script>
  