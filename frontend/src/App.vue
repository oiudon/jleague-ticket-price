<template>
  <v-app>
    <!-- ヘッダ -->
    <GlobalHeader />

    <!-- メインコンテンツ -->
    <RouterView />
  </v-app>
</template>

<script>
import { RouterView } from "vue-router";
import GlobalHeader from "./components/GlobalHeader.vue";

export default {
  name: "App",
  components: {
    GlobalHeader,
  },
};
</script>
