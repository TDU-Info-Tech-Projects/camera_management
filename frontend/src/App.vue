<template>
  <div id="app">
    <v-app app>
      <v-app-bar app>
        <v-toolbar-title style="width: 200px">備品レンタル</v-toolbar-title>
        <v-spacer></v-spacer>

        <v-tabs v-model="tab" align-with-title class="d-none d-sm-flex">
          <v-tab :to="'/'" v-if="store.user" link>
            備品一覧
          </v-tab>
          <v-tab :to="'/rented'" v-if="store.user" link>
            マイページ
          </v-tab>
          <v-tab :to="'/login'" v-if="!store.user" link>
            ログイン
          </v-tab>
          <v-tab :to="'/signup'" v-if="!store.user" link>
            新規登録
          </v-tab>
        </v-tabs>

        <v-btn color="warning" class="mr-4" @click="logout">
          ログアウト
        </v-btn>
      </v-app-bar>

      <!-- TODO: モバイルのメニュー項目を最後に更新 -->
      <v-navigation-drawer v-model="drawer" absolute temporary>
        <v-list nav>
          <v-list-item-group>
            <v-list-item :to="'/'" @click="tab = '/'; drawer = false" link>
              <v-list-item-title>備品一覧</v-list-item-title>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-navigation-drawer>

      <div style="margin-top:70px;">
        <router-view />
      </div>
    </v-app>
  </div>
</template>

<script>
import { store } from '@/store'

export default {
  data: () => ({
    drawer: false,
    store,
    tab: null,
  }),
  mounted: async () => {
  },
  methods: {
    async logout() {
      await store.logout()
      this.$router.push("/login")
    }
  }
}
</script>