<template>
  <v-dialog
    :max-width="width"
    persistent
    v-bind:value="show"
    @click:outside="closeDialog"
    @keydown.esc="closeDialog"
  >
    <v-card>
      <div class="dialog-body">
        <v-card-title class primary-title>
          <slot name="title"></slot>
        </v-card-title>
        <v-card-text>
          <div class="dialog-icon">
            <slot name="icon">
              <v-icon medium>default-icon</v-icon>
            </slot>
          </div>
          <div class="dialog-text">
            <slot name="text">default text</slot>
          </div>
        </v-card-text>
      </div>
      <v-card-actions class="justify-center">
        <div v-if="type === 'OK'">
          <v-btn class="mb-5" color="primary" depressed @click="closeDialog">
            <slot name="button-text">
              <span>OK</span>
            </slot>
          </v-btn>
        </div>
        <div v-else-if="type === 'CONTINUE'">
          <v-btn class="mb-5 mr-5" outlined @click="closeDialog">
            <slot name="button-text-cancel">
              <span>Cancel</span>
            </slot>
          </v-btn>
          <v-btn class="mb-5" color="primary" depressed @click="continueDialog">
            <slot name="button-text-continue">
              <span>Continue</span>
            </slot>
          </v-btn>
        </div>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'BaseDialog',
  methods: {
    closeDialog() {
      this.$emit('close-dialog');
    },
    continueDialog() {
      this.$emit('continue-dialog');
    }
  },
  props: {
    show: {
      default: false,
      type: Boolean
    },
    type: {
      default: 'OK',
      type: String
    },
    width: {
      default: '500',
      type: String
    }
  }
};
</script>

<style scoped>
.v-card__text {
  display: flex !important;
  padding: 1.5rem;
}
.dialog-icon {
  margin-right: 1rem;
  object-fit: contain;
  align-self: flex-start;
}
.dialog-text {
  flex: 1 1 auto;
  width: 90%;
}
</style>
