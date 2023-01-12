<template>
  <div v-if="authenticated">
    <div v-if="authorized()">
      <slot />
    </div>
    <div v-else class="text-center">
      <h1 class="my-8">You are not authorized to use this feature.</h1>
      <router-link :to="{ name: 'Home' }">
        <v-btn color="primary" class="about-btn" large>
          <v-icon left>mdi-home</v-icon>
          <span>Return</span>
        </v-btn>
      </router-link>
    </div>
  </div>
  <div v-else class="text-center">
    <h1 class="my-8">You must be logged in to use this feature.</h1>
    <v-btn v-if="keycloakReady" color="primary" class="login-btn" @click="login" large>
      <span>Login</span>
    </v-btn>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { AppRoles } from '@/utils/constants';

export default {
  name: 'BaseSecure',
  computed: {
    ...mapGetters('auth', [
      'authenticated',
      'createLoginUrl',
      'hasResourceRoles',
      'keycloakReady'
    ])
  },
  methods: {
    authorized() {
      const roles = [];
      if (this.testrole) roles.push(AppRoles.TESTROLE);
      return this.hasResourceRoles('app', roles);
    },
    login() {
      if (this.keycloakReady) {
        window.location.replace(this.createLoginUrl({ idpHint: 'idir' }));
      }
    }
  },
  props: {
    testrole: {
      default: false,
      type: Boolean
    }
  }
};
</script>
