<template>
  <v-footer class="gov-footer d-print-none">
    <v-btn text id="footer-home" href="https://www.gov.bc.ca/">
      <span>Home</span>
    </v-btn>
    <v-btn text id="footer-about" href="https://www2.gov.bc.ca/gov/content/about-gov-bc-ca">
      <span>About gov.bc.ca</span>
    </v-btn>
    <v-btn text id="footer-disclaimer" href="http://gov.bc.ca/disclaimer">
      <span>Disclaimer</span>
    </v-btn>
    <v-btn text id="footer-privacy" href="http://gov.bc.ca/privacy">
      <span>Privacy</span>
    </v-btn>
    <v-btn text id="footer-accessibility" href="http://gov.bc.ca/webaccessibility">
      <span>Accessibility</span>
    </v-btn>
    <v-btn text id="footer-copyright" href="http://gov.bc.ca/copyright">
      <span>Copyright</span>
    </v-btn>
    <v-btn text id="footer-contact" href="https://www2.gov.bc.ca/gov/content/home/contact-us">
      <span>Contact Us</span>
    </v-btn>
  </v-footer>
</template>

<script>
export default {
  name: 'BCGovFooter'
};
</script>

<style lang="scss" scoped>
.gov-footer {
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
