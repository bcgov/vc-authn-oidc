import { shallowMount } from '@vue/test-utils';

import HelloCall from '@/components/HelloCall.vue';
import helloService from '@/services/helloService';

describe('HelloCall.vue', () => {
  const getHelloSpy = jest.spyOn(helloService, 'getHello');

  beforeEach(() => {
    getHelloSpy.mockReset();
  });

  it('renders the page', () => {
    const wrapper = shallowMount(HelloCall, { stubs: ['BaseDialog'] });
    expect(wrapper.text()).toMatch('Get Response');
  });

  it('renders a success dialog on click', async () => {
    getHelloSpy.mockResolvedValue('test');

    const wrapper = shallowMount(HelloCall, { stubs: ['BaseDialog'] });
    await wrapper.vm.getHello();

    expect(wrapper.text()).toMatch('Get Response');
    expect(wrapper.vm.error).toBeFalsy();
    expect(wrapper.vm.showDialog).toBeTruthy();
  });

  it('renders a failure dialog on click', async () => {
    getHelloSpy.mockRejectedValue('test');

    const wrapper = shallowMount(HelloCall, { stubs: ['BaseDialog'] });
    await wrapper.vm.getHello();

    expect(wrapper.text()).toMatch('Get Response');
    expect(wrapper.vm.error).toBeTruthy();
    expect(wrapper.vm.showDialog).toBeTruthy();
  });
});
