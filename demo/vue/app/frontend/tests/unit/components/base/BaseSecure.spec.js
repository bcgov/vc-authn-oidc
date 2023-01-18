import { shallowMount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';

import BaseSecure from '@/components/base/BaseSecure.vue';

const localVue = createLocalVue();
localVue.use(Vuex);

describe('BaseSecure.vue', () => {
  const { location } = window;
  const mockReplace = jest.fn(cb => {
    cb();
  });
  let store;

  beforeAll(() => {
    delete window.location;
    window.location = {
      replace: mockReplace
    };
  });

  beforeEach(() => {
    mockReplace.mockReset();
    store = new Vuex.Store();
  });

  afterAll(() => {
    window.location = location;
  });

  it('renders nothing if authenticated and authorized', () => {
    store.registerModule('auth', {
      namespaced: true,
      getters: {
        authenticated: () => true,
        hasResourceRoles: () => () => true,
        keycloakReady: () => true
      }
    });

    const wrapper = shallowMount(BaseSecure, { localVue, store });

    expect(wrapper.text()).toMatch('');
  });

  it('renders a message if authenticated and unauthorized', () => {
    store.registerModule('auth', {
      namespaced: true,
      getters: {
        authenticated: () => true,
        hasResourceRoles: () => () => false,
        keycloakReady: () => true
      }
    });

    const wrapper = shallowMount(BaseSecure, {
      localVue,
      propsData: {
        admin: true
      },
      store,
      stubs: ['router-link']
    });

    expect(wrapper.text()).toMatch('You are not authorized to use this feature.');
  });

  it('renders a message with login button if unauthenticated', () => {
    store.registerModule('auth', {
      namespaced: true,
      getters: {
        authenticated: () => false,
        hasResourceRoles: () => () => false,
        keycloakReady: () => true
      }
    });

    const wrapper = shallowMount(BaseSecure, { localVue, store });

    expect(wrapper.text()).toMatch('You must be logged in to use this feature.');
  });

  it('renders a message without login button if unauthenticated', () => {
    store.registerModule('auth', {
      namespaced: true,
      getters: {
        authenticated: () => false,
        hasResourceRoles: () => () => false,
        keycloakReady: () => false
      }
    });

    const wrapper = shallowMount(BaseSecure, { localVue, store });

    expect(wrapper.text()).toMatch('You must be logged in to use this feature.');
  });

  it('login button redirects to login url', () => {
    store.registerModule('auth', {
      namespaced: true,
      getters: {
        authenticated: () => false,
        createLoginUrl: () => () => 'test',
        keycloakReady: () => true
      }
    });

    const wrapper = shallowMount(BaseSecure, { localVue, store });
    wrapper.vm.login();

    expect(wrapper.text()).toMatch('Login');
    expect(mockReplace).toHaveBeenCalledTimes(1);
  });
});
