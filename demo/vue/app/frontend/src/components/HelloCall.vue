<template>
  <v-container class="text-center">
    <v-btn @click="getHello" color="primary" large :loading="loading">
      <v-icon left>mdi-hexagon-multiple</v-icon>
      <span>Get Response</span>
    </v-btn>

    <BaseDialog :show="showDialog" @close-dialog="showDialog = false">
      <template v-slot:icon>
        <v-icon v-if="!error" large color="success">info</v-icon>
        <v-icon v-else large color="error">warning</v-icon>
      </template>
      <template v-slot:text>
        <p>{{ helloData }}</p>
      </template>
    </BaseDialog>
  </v-container>
</template>

<script>
import helloService from '@/services/helloService';

export default {
  name: 'HelloWorld',
  data: () => ({
    error: false,
    helloData: '',
    loading: false,
    showDialog: false
  }),
  methods: {
    async getHello() {
      this.error = false;
      this.loading = true;
      try {
        const response = await helloService.getHello();
        this.helloData = response.data;
      } catch (e) {
        this.error = true;
        this.helloData = e;
      }
      this.loading = false;
      this.showDialog = true;
    }
  }
};
</script>



