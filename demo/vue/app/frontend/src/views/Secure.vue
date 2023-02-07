<template>
  <v-container>
    <BaseSecure>
      <h1 class="my-6 text-center">Secure</h1>
      <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed
        sollicitudin semper nunc, sed mollis turpis egestas at. Sed ornare,
        justo non facilisis ullamcorper, eros libero semper ligula, in euismod
        quam massa et dui. In vel lectus molestie, cursus urna id, vehicula
        felis. Mauris nec suscipit eros, vel vestibulum ex. Aenean vel gravida
        nulla. Morbi vel felis at arcu molestie faucibus vitae ut lacus. Nulla
        feugiat mi quis lectus aliquet, sit amet tristique magna pharetra.
        Mauris quis felis blandit est hendrerit vulputate.
      </p>
      <HelloCall />

      <div v-if="tokenParsed.pres_req_conf_id != presReqConfId">
        INVALID LOGIN
      </div>
      <div v-else>Login Valid</div>

      <pre>{{ JSON.stringify(tokenParsed, null, 2) }}</pre>

      <ul>
        <li>If something in the verification configuration is missing, ensure it is being imported to the Keycloak user
          by the Identity Provider Mapper here. </li>
        <li><a
          href="http://localhost:8880/auth/admin/master/console/#/realms/vc-authn/identity-provider-mappers/vc-authn/mappers">http://localhost:8880/auth/admin/master/console/#/realms/vc-authn/identity-provider-mappers/vc-authn/mappers</a>
        </li>
        <li>and ensure is being added to the token by the client mappers here (click the link, then the 'vue-fe' client,
          then the 'Mappers' tab). </li>
        <li><a
          href="http://localhost:8880/auth/admin/master/console/#/realms/vc-authn/clients/">http://localhost:8880/auth/admin/master/console/#/realms/vc-authn/clients/4f4d8312-bdd0-4539-8c51-f8de81cf5f41/mapper</a>
        </li>
      </li>



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
