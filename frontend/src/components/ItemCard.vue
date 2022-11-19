<template>
  <v-card :loading="loading" class="mx-auto my-12" max-width="300">

    <v-img height="200" :src="imageUrl"></v-img>

    <v-card-title>{{title}}</v-card-title>

    <v-divider class="mx-4"></v-divider>

    <v-card-actions>
      <v-btn color="deep-purple" text @click="reserve">
        予約
      </v-btn>
      <v-btn color="deep-purple" text @click="reserve">
        編集
      </v-btn>
      <v-btn color="deep-purple" text @click="reserve">
        削除
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
  
<script>
export default {
  props: {
    title: String,
    imageUrl: String,
    itemId: Number
  },
  data: () => ({
    loading: false,
    selection: 1,
  }),

  methods: {
    reserve() {
    },
  },
}
</script>
  