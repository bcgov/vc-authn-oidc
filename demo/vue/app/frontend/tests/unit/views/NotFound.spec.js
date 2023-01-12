import { shallowMount } from '@vue/test-utils';
import Vuetify from 'vuetify';
import VueRouter from 'vue-router';

import NotFound from '@/views/NotFound.vue';

describe('NotFound.vue', () => {
  let router;
  let vuetify;

  beforeEach(() => {
    router = new VueRouter();
    vuetify = new Vuetify();
  });

  it('renders', () => {
    const wrapper = shallowMount(NotFound, {
      vuetify,
      router,
      stubs: ['router-link', 'router-view']
    });

    expect(wrapper.text()).toMatch('404: Page not found. :(');
  });
});
