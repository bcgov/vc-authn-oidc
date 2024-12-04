<template>
  <v-footer class="owf-footer d-print-none">
    <v-btn text id="footer-home" href="https://openwallet.foundation">
      <span>Home</span>
    </v-btn>
    <v-btn text id="footer-about" href="https://openwallet.foundation/governing-board">
      <span>About OpenWallet Foundation</span>
    </v-btn>
    <v-btn text id="footer-disclaimer" href="https://openwallet.foundation/participate">
      <span>Participate</span>
    </v-btn>
    <v-btn text id="footer-privacy" href="https://openwallet.foundation/projects">
      <span>Projects</span>
    </v-btn>
  </v-footer>
</template>

<script>
export default {
  name: 'OWFFooter'
};
</script>

<style lang="scss" scoped>
.owf-footer {
  background-color: #003366 !important;
  border-top: 2px solid #fcba19;
  flex-shrink: 0;
  min-height: 2.5rem;
  min-width: 100%;
  padding-bottom: 0;
  padding-top: 0;

  a {
    color: #ffffff;
    font-size: 1rem;
    &:focus {
      outline: none;
    }
  }

  .v-btn__content > span {
    color: #ffffff;
    font-size: 1rem;
    font-weight: normal;
    text-decoration: none;
    text-transform: none;
  }
}
</style>
