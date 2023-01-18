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

      {{ tokenParsed }}
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
