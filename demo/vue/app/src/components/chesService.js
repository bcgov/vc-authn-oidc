const config = require('config');

const ClientConnection = require('./clientConnection');
const errorToProblem = require('./errorToProblem');
const log = require('./log')(module.filename);

const SERVICE = 'CHES';

class ChesService {
  constructor({tokenUrl, clientId, clientSecret, apiUrl}) {
    log.verbose(`Constructed with ${tokenUrl}, ${clientId}, clientSecret, ${apiUrl}`, { function: 'constructor' });
    if (!tokenUrl || !clientId || !clientSecret || !apiUrl) {
      log.error('Invalid configuration.', { function: 'constructor' });
      throw new Error('ChesService is not configured. Check configuration.');
    }
    this.connection = new ClientConnection({ tokenUrl, clientId, clientSecret });
    this.axios = this.connection.axios;
    this.apiUrl = apiUrl;
    this.apiV1 = `${this.apiUrl}/v1`;
  }

  async health() {
    try {
      const response = await this.axios.get(
        `${this.apiV1}/health`,
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      return response.data;
    } catch (e) {
      errorToProblem(SERVICE, e);
    }
  }

  async statusQuery(params) {
    try {
      const response = await this.axios.get(
        `${this.apiV1}/status`,
        {
          params: params,
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      return response.data;
    } catch (e) {
      errorToProblem(SERVICE, e);
    }
  }

  async cancelMsg(msgId) {
    try {
      const response = await this.axios.delete(
        `${this.apiV1}/cancel/${msgId}`,
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      return response.data;
    } catch (e) {
      errorToProblem(SERVICE, e);
    }
  }

  async cancelQuery(params) {
    try {
      const response = await this.axios.delete(
        `${this.apiV1}/cancel`,
        {
          params: params,
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      return response.data;
    } catch (e) {
      errorToProblem(SERVICE, e);
    }
  }

  async send(email) {
    try {
      const response = await this.axios.post(
        `${this.apiV1}/email`,
        email,
        {
          headers: {
            'Content-Type': 'application/json'
          },
          maxContentLength: Infinity,
          maxBodyLength: Infinity
        }
      );
      return response.data;
    } catch (e) {
      errorToProblem(SERVICE, e);
    }
  }


  async merge(data) {
    try {
      const response = await this.axios.post(
        `${this.apiV1}/emailMerge`,
        data,
        {
          headers: {
            'Content-Type': 'application/json'
          },
          maxContentLength: Infinity,
          maxBodyLength: Infinity
        }
      );
      return response.data;
    } catch (e) {
      errorToProblem(SERVICE, e);
    }
  }

  async preview(data) {
    try {
      const response = await this.axios.post(
        `${this.apiV1}/emailMerge/preview`,
        data,
        {
          headers: {
            'Content-Type': 'application/json'
          },
          maxContentLength: Infinity,
          maxBodyLength: Infinity
        }
      );
      return response.data;
    } catch (e) {
      errorToProblem(SERVICE, e);
    }
  }

}

const endpoint = config.get('serviceClient.commonServices.ches.endpoint');
const tokenEndpoint = config.get('serviceClient.commonServices.tokenEndpoint');
const username = config.get('serviceClient.commonServices.username');
const password = config.get('serviceClient.commonServices.password');

let chesService = new ChesService({tokenUrl: tokenEndpoint, clientId: username, clientSecret: password, apiUrl: endpoint});
module.exports = chesService;
