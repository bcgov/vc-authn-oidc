import { shallowMount } from '@vue/test-utils';
import BCGovFooter from '@/components/bcgov/BCGovFooter.vue';

describe('BCGovFooter.vue', () => {
  it('renders', () => {
    const wrapper = shallowMount(BCGovFooter);
    expect(wrapper.text()).toMatch('About gov.bc.ca');
  });
});
