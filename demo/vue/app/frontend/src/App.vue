<template>
  <v-app>
    <OWFHeader />
    <OWFNavBar />

    <v-main>
      <transition name="component-fade" mode="out-in">
        <router-view />
      </transition>
    </v-main>

    <OWFFooter />
  </v-app>
</template>

<script>
import OWFHeader from '@/components/owf/OWFHeader.vue';
import OWFFooter from '@/components/owf/OWFFooter.vue';
import OWFNavBar from '@/components/owf/OWFNavBar.vue';

export default {
  name: 'App',
  components: {
    OWFHeader,
    OWFFooter,
    OWFNavBar
  }
};
</script>

<style scoped>
.component-fade-enter-active,
.component-fade-leave-active {
  transition: opacity 0.3s ease;
}
.component-fade-enter,
.component-fade-leave-to {
  opacity: 0;
}
</style>
