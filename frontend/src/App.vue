<template>
  <div id="app">
    <v-app app>
      <v-app-bar app>
        <v-app-bar-nav-icon @click="drawer = true" class="d-flex d-sm-none"></v-app-bar-nav-icon>
        <v-toolbar-title>Your Dashboard</v-toolbar-title>
        <v-spacer></v-spacer>
  
        <v-btn icon>
          <v-icon>mdi-magnify</v-icon>
        </v-btn>
  
        <v-btn icon>
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
  
        <template v-slot:extension>
          <v-tabs v-model="tab" align-with-title class="d-none d-sm-flex">
            <v-tabs-slider color="yellow"></v-tabs-slider>
  
            <v-tab v-for="[icon, text, to] in links" :key="icon" :to="to" link>
              {{ text }}
            </v-tab>
          </v-tabs>
        </template>
      </v-app-bar>
      <!-- Add a navigation bar -->
      <v-navigation-drawer v-model="drawer" absolute temporary>
        <v-list nav dense>
          <v-list-item-group>
            <v-list-item v-for="[icon, text, to] in links" :key="icon" :to="to" link>
              <v-list-item-title @click="tab = index">{{ text }}</v-list-item-title>
            </v-list-item>
  
          </v-list-item-group>
        </v-list>
      </v-navigation-drawer>
      <!-- Navigation bar ends -->
        <div style="margin-top:130px;">
          <router-view />
        </div>
    </v-app>
  </div>

</template>

<script>
export default {
  data: () => ({
    drawer: false,
    tab: null,
    items: [
      'web', 'shopping', 'videos', 'images', 'news',
    ],
    links: [
      ['mdi-inbox-arrow-down', 'Inbox', '/'],
      ['mdi-send', 'about', '/about'],
      ['mdi-delete', 'charts', '/charts'],
      ['mdi-alert-octagon', 'admin', '/admin'],
      ['mdi-alert-octagon2', 'list', '/lists'],
    ],

  })
}
</script>