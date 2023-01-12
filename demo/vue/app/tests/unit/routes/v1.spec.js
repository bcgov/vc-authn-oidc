const request = require('supertest');

const { expressHelper } = require('../../common/helper');
const router = require('../../../src/routes/v1');

// Simple Express Server
const basePath = '/api/v1';
const app = expressHelper(basePath, router);

describe(`GET ${basePath}`, () => {
  it('should return all available endpoints', async () => {
    const response = await request(app).get(`${basePath}`);

    expect(response.statusCode).toBe(200);
    expect(response.body).toBeTruthy();
    expect(Array.isArray(response.body.endpoints)).toBeTruthy();
    expect(response.body.endpoints).toHaveLength(2);
    expect(response.body.endpoints).toContain('/docs');
    expect(response.body.endpoints).toContain('/hello');
  });
});

describe(`GET ${basePath}/docs`, () => {
  it('should return a redoc html page', async () => {
    const response = await request(app).get(`${basePath}/docs`);

    expect(response.statusCode).toBe(200);
    expect(response.text).toContain('<title>Vue Skeleton API - Documentation');
  });
});

describe(`GET ${basePath}/api-spec.yaml`, () => {
  it('should return the OpenAPI spec in yaml', async () => {
    const response = await request(app).get(`${basePath}/api-spec.yaml`);

    expect(response.statusCode).toBe(200);
    expect(response.body).toBeTruthy();
    expect(response.headers['content-type']).toBeTruthy();
    expect(response.headers['content-type']).toMatch('application/yaml; charset=utf-8');
    expect(response.text).toContain('openapi: 3.0.3');
    expect(response.text).toContain('title: Vue Skeleton API');
  });
});

describe(`GET ${basePath}/api-spec.json`, () => {
  it('should return the OpenAPI spec in json', async () => {
    const response = await request(app).get(`${basePath}/api-spec.json`);

    expect(response.statusCode).toBe(200);
    expect(response.headers['content-type']).toBeTruthy();
    expect(response.headers['content-type']).toMatch('application/json; charset=utf-8');
    expect(response.body).toBeTruthy();
    expect(response.body.openapi).toMatch('3.0.3');
    expect(response.body.info.title).toMatch('Vue Skeleton API');
  });
});
