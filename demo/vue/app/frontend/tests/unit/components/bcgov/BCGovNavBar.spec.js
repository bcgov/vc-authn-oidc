import { shallowMount } from '@vue/test-utils';
import Vuetify from 'vuetify';
import VueRouter from 'vue-router';

import BCGovNavBar from '@/components/bcgov/BCGovNavBar.vue';

describe('BCGovNavBar.vue', () => {
  let router;
  let vuetify;

  beforeEach(() => {
    router = new VueRouter();
    vuetify = new Vuetify();
  });

  it('renders', () => {
    const wrapper = shallowMount(BCGovNavBar, {
      vuetify,
      router,
      stubs: ['router-link', 'router-view']
    });

    expect(wrapper.text()).toContain('Home');
    expect(wrapper.text()).toContain('Secure');
  });
});
