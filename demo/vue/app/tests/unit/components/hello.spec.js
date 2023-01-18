const hello = require('../../../src/components/hello');

describe('getHello', () => {
  it('should return a string', () => {
    const result = hello.getHello();

    expect(result).toBeTruthy();
    expect(result).toMatch('Hello World!');
  });
});
