<template>
  <v-card :loading="loading" class="mx-auto" max-width="300" :disabled="item.stock <= 0">

    <v-img height="200" :src="item.image_url"></v-img>

    <v-card-title>{{ item.name }}</v-card-title>

    <v-card-text>{{ item.description.slice(0, 34) + '...' }}</v-card-text>

    <v-divider class="mx-4"></v-divider>

    <v-card-actions>
      <v-btn color="primary" depressed @click="reserveDialog" disabled v-if="item.stock <= 0">
        {{ item.is_consumable ? '在庫なし' : '貸出中' }}
      </v-btn>

      <v-btn color="primary" depressed @click="reserveDialog" v-else>
        {{ buyOrRent }} {{ item.stock > 0 && item.is_consumable ? `(在庫数: ${item.stock})` : '' }}
      </v-btn>
    </v-card-actions>

    <v-dialog v-model="dialog" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ item.name }}の{{ buyOrRent }}</span>
        </v-card-title>
        <v-img :src="item.image_url" height="300" class="transparent" contain />
        <v-card-text style="margin-top: 30px;">
          {{ item.description }}
        </v-card-text>
        <v-card-text v-if="!item.is_consumable">
          <v-container>
            <v-row>
              <v-col cols="24">
                <v-card-title>返却日{{ requireLensSelect ? 'とレンズ' : '' }}を選択してください。</v-card-title>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" sm="6">
                <v-select :items="dateOptions" v-model="dueDate" label="返却日*" required />
              </v-col>
              <v-col cols="12" sm="6" v-if="requireLensSelect">
                <v-select :items="lensOptions" v-model="lensId" label="レンズ*" required />
              </v-col>
            </v-row>
          </v-container>
          <small>*必須項目</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="reset">
            キャンセル
          </v-btn>
          <v-btn color="blue darken-1" text @click="reserve">
            {{ buyOrRent }}確定
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>
  
<script>
import { store } from '@/store'
import { httpUtils, paths, dateStringFormat } from '@/utils'

export default {
  props: {
    item: Object,
    allItems: Array
  },
  data: () => ({
    loading: false,
    store,
    dialog: false,
    dateOptions: [],
    lensOptions: [],
    lensId: null,
    dueDate: null,
  }),

  computed: {
    requireLensSelect() {
      const item = this.$props.item
      if (item.is_lens) {
        return false
      }
      if (!item.mount_id || item.is_consumable) {
        return false
      }
      
      return true
    },
    buyOrRent() {
      return this.$props.item.is_consumable ? '購入' : 'レンタル'
    }
  },

  methods: {
    dateStringFormat,
    async reserveDialog() {
      try {
        this.loading = true
        this.dateOptions = []
        this.lensOptions = []

        let now = new Date()
        let dateOptions = []
        for (let i = 0; i < 14; i++) {
          now.setDate(now.getDate() + 1)
          dateOptions.push(now.toISOString().slice(0, 10))
        }
        this.dateOptions = dateOptions

        let lensOptions = [{
          text: "カメラ本体のみ",
          value: null
        }]

        for (const item of this.allItems) {
          if (item.is_lens && this.$props.item.mount_id == item.mount_id)
            lensOptions.push({
              text: item.name,
              value: item.id
            })
        }
        this.lensOptions = lensOptions

        this.dialog = true
      } finally {
        this.loading = false
      }
    },
    async confirmReserve() {
      try {
        const item = this.$props.item

        if (!item.is_consumable && !this.dueDate) {
          this.$swal({
            icon: 'error',
            title: '返却日を選択してください'
          })
          return
        }

        let rentItems = [item.id]
        if (!item.is_lens && !item.is_consumable && this.lensId) {
          rentItems.push(this.lensId)
        }
        const res = await fetch(paths.itemRent, httpUtils.post({
          ids: rentItems,
          due_date: this.dueDate
        }))
        if (res.ok) {
          this.reset()
          this.$swal({
            icon: 'success',
            text: `${this.buyOrRent}が完了しました。${this.buyOrRent}内容はマイページからご確認頂けます。`,
            allowOutsideClick: false
          }).then(() => {
            location.reload()
          })
        } else {
          throw res
        }
      } catch {
        this.$swal({
          icon: 'error',
          text: 'エラーが発生しました。もう一度お試しください。'
        })
      }
    },
    async reserve() {
      const item = this.$props.item

      if (this.requireLensSelect && !this.lensId) {
        this.$swal({
          icon: 'warning',
          title: '本体のみのレンタルでよろしいですか。',
          text: '本商品は本体のみではご利用できません、レンズが必要になります。',
          showCancelButton: true,
          cancelButtonText: '戻る',
          confirmButtonText: '本体のみレンタル',
          reverseButtons: true
        }).then(result => {
          if (result.isConfirmed) {
            this.confirmReserve()
          }
        })
      } else {
        this.confirmReserve()
      }
    },
    reset() {
      this.dialog = false
    }
  },
  mounted() {

  }
}
</script>
