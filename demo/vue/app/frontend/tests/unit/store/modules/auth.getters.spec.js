import { cloneDeep } from 'lodash';
import { createLocalVue } from '@vue/test-utils';
import Vue from 'vue';
import Vuex from 'vuex';

import authStore from '@/store/modules/auth';
import { AppRoles } from '@/utils/constants';

const localVue = createLocalVue();
localVue.use(Vuex);

const zeroUuid = '00000000-0000-0000-0000-000000000000';

const keycloakHelper = (mockKcObject) => {
  // TODO: Find better way to set up keycloak object mock without deleting first
  if (Vue.prototype.$keycloak) {
    delete Vue.prototype.$keycloak;
  }
  Object.defineProperty(Vue.prototype, '$keycloak', {
    configurable: true, // Needed to allow deletions later
    get() {
      return mockKcObject;
    }
  });
};

describe('auth getters', () => {
  let authenticated;
  let roles;
  let store;

  beforeEach(() => {
    authenticated = true;
    roles = [];
    store = new Vuex.Store(cloneDeep(authStore));

    Object.defineProperty(Vue.prototype, '$keycloak', {
      configurable: true, // Needed to allow deletions later
      get() {
        return {
          authenticated: authenticated,
          createLoginUrl: () => 'loginUrl',
          createLogoutUrl: () => 'logoutUrl',
          fullName: 'fName',
          ready: true,
          subject: zeroUuid,
          token: 'token',
          tokenParsed: {
            email: 'e@mail.com',
            identity_provider: 'idir',
            realm_access: {},
            resource_access: {
              app: {
                roles: roles
              }
            }
          },
          userName: 'uName'
        };
      }
    });
  });

  afterEach(() => {
    if (Vue.prototype.$keycloak) {
      delete Vue.prototype.$keycloak;
    }
  });

  it('authenticated should return a boolean', () => {
    expect(store.getters.authenticated).toBeTruthy();
  });

  it('createLoginUrl should return a string', () => {
    expect(store.getters.createLoginUrl).toBeTruthy();
    expect(typeof store.getters.createLoginUrl).toBe('function');
    expect(store.getters.createLoginUrl()).toMatch('loginUrl');
  });

  it('createLogoutUrl should return a string', () => {
    expect(store.getters.createLogoutUrl).toBeTruthy();
    expect(typeof store.getters.createLogoutUrl).toBe('function');
    expect(store.getters.createLogoutUrl()).toMatch('logoutUrl');
  });

  it('email should return a string', () => {
    expect(store.getters.email).toBeTruthy();
    expect(store.getters.email).toMatch('e@mail.com');
  });

  it('email should return an empty string', () => {
    keycloakHelper({
      tokenParsed: undefined
    });

    expect(store.getters.email).toBeFalsy();
    expect(store.getters.email).toEqual('');
  });

  it('fullName should return a string', () => {
    expect(store.getters.fullName).toBeTruthy();
    expect(store.getters.fullName).toMatch('fName');
  });

  it('hasResourceRoles should return false if unauthenticated', () => {
    authenticated = false;

    expect(store.getters.authenticated).toBeFalsy();
    expect(store.getters.hasResourceRoles('app', roles)).toBeFalsy();
  });

  it('hasResourceRoles should return true when checking no roles', () => {
    authenticated = true;
    roles = [];

    expect(store.getters.authenticated).toBeTruthy();
    expect(store.getters.hasResourceRoles('app', roles)).toBeTruthy();
  });

  it('hasResourceRoles should return true when role exists', () => {
    authenticated = true;
    roles = [AppRoles.TESTROLE];

    expect(store.getters.authenticated).toBeTruthy();
    expect(store.getters.hasResourceRoles('app', roles)).toBeTruthy();
  });

  it('hasResourceRoles should return false when resource does not exist', () => {
    authenticated = true;
    roles = ['non-existent-role'];

    keycloakHelper({
      authenticated: authenticated,
      tokenParsed: {
        realm_access: {},
        resource_access: {}
      }
    });

    expect(store.getters.authenticated).toBeTruthy();
    expect(store.getters.hasResourceRoles('app', roles)).toBeFalsy();
  });

  it('identityProvider should return a string', () => {
    expect(store.getters.identityProvider).toBeTruthy();
    expect(typeof store.getters.identityProvider).toBe('string');
  });

  it('keycloakReady should return a boolean', () => {
    expect(store.getters.keycloakReady).toBeTruthy();
  });

  it('keycloakSubject should return a string', () => {
    expect(store.getters.keycloakSubject).toBeTruthy();
    expect(store.getters.keycloakSubject).toMatch(zeroUuid);
  });

  it('moduleLoaded should return a boolean', () => {
    expect(store.getters.moduleLoaded).toBeTruthy();
  });

  it('realmAccess should return an object', () => {
    expect(store.getters.realmAccess).toBeTruthy();
    expect(typeof store.getters.realmAccess).toBe('object');
  });

  it('realmAccess should return a string', () => {
    const uri = 'http://foo.bar';
    store.replaceState({ redirectUri: uri });

    expect(store.getters.redirectUri).toBeTruthy();
    expect(typeof store.getters.redirectUri).toBe('string');
    expect(store.getters.redirectUri).toEqual(uri);
  });

  it('resourceAccess should return an object', () => {
    expect(store.getters.resourceAccess).toBeTruthy();
    expect(typeof store.getters.resourceAccess).toBe('object');
  });

  it('token should return a string', () => {
    expect(store.getters.token).toBeTruthy();
    expect(store.getters.token).toMatch('token');
  });

  it('tokenParsed should return an object', () => {
    expect(store.getters.tokenParsed).toBeTruthy();
    expect(typeof store.getters.tokenParsed).toBe('object');
  });

  it('userName should return a string', () => {
    expect(store.getters.userName).toBeTruthy();
    expect(store.getters.userName).toMatch('uName');
  });
});
