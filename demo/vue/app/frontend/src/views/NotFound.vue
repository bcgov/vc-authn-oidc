<template>
  <v-container class="text-center">
    <h1 class="my-6">404: Page not found. :(</h1>
    <router-link :to="{ name: 'Home' }">
      <v-btn color="primary" large>
        <v-icon left>mdi-home</v-icon>
        <span>Home</span>
      </v-btn>
    </router-link>
  </v-container>
</template>

<script>
export default {
  name: 'NotFound'
};
</script>
