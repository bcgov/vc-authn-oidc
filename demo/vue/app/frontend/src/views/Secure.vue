<template>
  <v-container>
    <BaseSecure>
      <h1 class="my-6 text-center">Secure</h1>
      <HelloCall />

      <div v-if="tokenParsed.pres_req_conf_id != presReqConfId">
        INVALID LOGIN
      </div>
      <div v-else>Login Valid</div>

      <pre>{{ JSON.stringify(tokenParsed, null, 2) }}</pre>

      <ul>
        <li>
          If something in the verification configuration is missing, ensure it
          is being imported to the Keycloak user by the Identity Provider Mapper
          here.
        </li>
        <li>
          <a
            href="http://localhost:8880/auth/admin/master/console/#/realms/vc-authn/identity-provider-mappers/vc-authn/mappers"
          >http://localhost:8880/auth/admin/master/console/#/realms/vc-authn/identity-provider-mappers/vc-authn/mappers
          </a>
        </li>
        <li>
          and ensure is being added to the token by the client mappers here
          (click the link, then the 'vue-fe' client, then the 'Mappers' tab).
        </li>
        <li>
          <a
            href="http://localhost:8880/auth/admin/master/console/#/realms/vc-authn/clients/"
          >http://localhost:8880/auth/admin/master/console/#/realms/vc-authn/clients/4f4d8312-bdd0-4539-8c51-f8de81cf5f41/mapper</a
          >
        </li>
      </ul>
    </BaseSecure>
  </v-container>
</template>

<script>
import HelloCall from '@/components/HelloCall';
import { mapGetters } from 'vuex';

export default {
  name: 'Secure',
  components: {
    HelloCall,
  },
  computed: {
    ...mapGetters('auth', ['tokenParsed', 'presReqConfId']),
  },
};
</script>
