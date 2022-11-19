<template>
  <v-card :loading="loading" class="mx-auto my-12" max-width="300" :disabled="item.stock <= 0">

    <v-img height="200" :src="item.image_url"></v-img>

    <v-card-title>{{ item.name }}</v-card-title>

    <v-card-text>
      <v-chip active :color="item.stock > 0 ? 'deep-purple' : 'red'" text-color="white">
        {{ item.stock > 0 ? item.is_consumable ? '購入可' : '貸出可' : item.is_consumable ? '在庫なし' : '貸出中' }}
      </v-chip>
    </v-card-text>

    <v-divider class="mx-4"></v-divider>

    <v-card-actions>
      <v-btn color="deep-purple" text @click="reserveDialog" :disabled="item.stock <= 0">
        予約
      </v-btn>
      <v-btn color="deep-purple" text @click="" v-if="store.user.is_admin">
        編集
      </v-btn>
      <v-btn color="deep-purple" text @click="" v-if="store.user.is_admin">
        削除
      </v-btn>
    </v-card-actions>

    <v-dialog v-model="dialog" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ item.name }}のレンタル・購入</span>
        </v-card-title>
        <v-img :src="item.image_url" height="300" class="transparent" contain />
        <v-card-text style="margin-top: 30px;">
          {{ item.description }}
        </v-card-text>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="24">
                <v-card-title>返却日とレンズを選択してください。</v-card-title>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" sm="6">
                <v-select :items="['0-17', '18-29', '30-54', '54+']" label="Age*" required></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select :items="['0-17', '18-29', '30-54', '54+']" label="Age*" required></v-select>
              </v-col>
            </v-row>
          </v-container>
          <small>*必須項目</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">
            閉じる
          </v-btn>
          <v-btn color="blue darken-1" text @click="dialog = false">
            予約
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>
  
<script>
import { store } from '@/store'

export default {
  props: {
    item: Object
  },
  data: () => ({
    loading: false,
    selection: 1,
    store,
    dialog: true
  }),

  methods: {
    reserveDialog() {
      this.dialog = true
    },
  },
}
</script>
  