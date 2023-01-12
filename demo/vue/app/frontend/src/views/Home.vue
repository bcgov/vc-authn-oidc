<template>
  <v-container>
    <h1 class="my-6 text-center">
      Welcome to Vuetify - Now deployed with GitHub Actions v2
    </h1>
    <HelloWorld />
  </v-container>
</template>

<script>
import HelloWorld from '@/components/HelloWorld.vue';
export default {
  name: 'Home',
  components: {
    HelloWorld,
  },
};
</script>
