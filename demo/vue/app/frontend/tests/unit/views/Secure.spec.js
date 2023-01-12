import { shallowMount } from '@vue/test-utils';
import Vuetify from 'vuetify';

import Secure from '@/views/Secure.vue';

describe('Secure.vue', () => {
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('renders', () => {
    const wrapper = shallowMount(Secure, {
      vuetify,
      stubs: ['BaseSecure']
    });

    expect(wrapper.text()).toMatch('');
  });
});
