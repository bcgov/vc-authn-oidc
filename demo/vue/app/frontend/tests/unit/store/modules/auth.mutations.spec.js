import { cloneDeep } from 'lodash';

import store from '@/store/modules/auth';

describe('auth mutations', () => {
  let state;

  beforeEach(() => {
    state = cloneDeep(store.state);
  });

  it('SET_REDIRECTURI should update redirecturi', () => {
    const uri = 'http://foo.bar';
    store.mutations.SET_REDIRECTURI(state, uri);

    expect(state.redirectUri).toBeTruthy();
    expect(state.redirectUri).toEqual(uri);
  });
});
