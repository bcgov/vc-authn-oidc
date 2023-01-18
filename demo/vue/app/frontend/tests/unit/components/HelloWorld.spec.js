import { shallowMount } from '@vue/test-utils';
import HelloWorld from '@/components/HelloWorld.vue';

describe('HelloWorld.vue', () => {
  it('renders', () => {
    const wrapper = shallowMount(HelloWorld);
    expect(wrapper.text()).toMatch('Vuetify');
  });
});
