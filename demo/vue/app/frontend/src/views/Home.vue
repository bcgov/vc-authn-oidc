<template>
  <v-container>
    <h1 class="my-6 text-center">Welcome to vc-authn-oidc demo application.</h1>
    <h2>Pre-requisites</h2>
    <br />
    <h4>Mobile Wallet</h4>
    <ul>
      <li>
        Download BC Wallet to a mobile device
        <a
          href="https://www2.gov.bc.ca/gov/content/governments/government-id/bc-wallet"
          >https://www2.gov.bc.ca/gov/content/governments/government-id/bc-wallet</a
        >
      </li>
      <li>
        Connect to an issuer and issue your wallet a credential with the fields
        "first_name" and "last_name".
      </li>
    </ul>
    <br />

    <h4>ACA-Py Wallet:</h4>
    <ul>
      <li>
        Wallet needs a public did (for connectionless present-proof requests)
      </li>
    </ul>
    <br />

    <h4>Controller/Keycloak Configuration</h4>
    <ul>
      <li>
        Navigate to the controller
        <a href="http://localhost:5201/docs">swagger</a> and POST to
        '/ver_configs' with the default payload
      </li>
      <li>
        Navigate to the
        <a
          href="http://localhost:8880/auth/admin/master/console/#/realms/vc-authn/identity-provider-settings/provider/oidc/vc-authn"
          >keycloak idp config</a
        >
        and set the client secret to "12345678"
      </li>
      <li>
        Click "Login" in the top right, then click "Verifiable Credential
        Access"
      </li>
    </ul>
    <br />
    <br />

    <h5>
      Any improvements to the demo setup to reduce/streamline these steps are
      great tasks for future developers
    </h5>
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
