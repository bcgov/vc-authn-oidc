const request = require('supertest');

const { expressHelper } = require('../../../common/helper');
const router = require('../../../../src/routes/v1/hello');

const helloComponent = require('../../../../src/components/hello');

// Simple Express Server
const basePath = '/api/v1/hello';
const app = expressHelper(basePath, router);

describe(`GET ${basePath}`, () => {
  const getHelloSpy = jest.spyOn(helloComponent, 'getHello');

  afterEach(() => {
    getHelloSpy.mockReset();
  });

  it('should yield a created response', async () => {
    getHelloSpy.mockReturnValue('test');

    const response = await request(app).get(`${basePath}`);

    expect(response.statusCode).toBe(200);
    expect(response.body).toBeTruthy();
    expect(response.body).toMatch('test');
    expect(getHelloSpy).toHaveBeenCalledTimes(1);
  });

  it('should yield an error and fail gracefully', async () => {
    getHelloSpy.mockImplementation(() => {
      throw new Error('bad');
    });

    const response = await request(app).get(`${basePath}`);

    expect(response.statusCode).toBe(500);
    expect(response.body).toBeTruthy();
    expect(response.body.details).toBe('bad');
    expect(getHelloSpy).toHaveBeenCalledTimes(1);
  });
});
