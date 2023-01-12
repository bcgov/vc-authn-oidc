const config = require('config');
const crypto = require('crypto');
const FormData = require('form-data');
const fs = require('fs-extra');

const ClientConnection = require('./clientConnection');
const errorToProblem = require('./errorToProblem');
const log = require('./log')(module.filename);

const SERVICE = 'CDOGS';

class CdogsService {
  constructor({ tokenUrl, clientId, clientSecret, apiUrl }) {
    log.verbose(`Constructed with ${tokenUrl}, ${clientId}, clientSecret, ${apiUrl}`, { function: 'constructor' });
    if (!tokenUrl || !clientId || !clientSecret || !apiUrl) {
      log.error('Invalid configuration.', { function: 'constructor' });
      throw new Error('CdogsService is not configured. Check configuration.');
    }
    this.connection = new ClientConnection({ tokenUrl, clientId, clientSecret });
    this.axios = this.connection.axios;
    this.apiUrl = apiUrl;
    this.apiV2 = `${this.apiUrl}/v2`;
  }

  async health() {
    try {
      const url = `${this.apiV2}/health`;
      log.debug(`GET to ${url}`, { function: 'health' });

      const { data, status } = await this.axios.get(url, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      return { data, status };
    } catch (e) {
      errorToProblem(SERVICE, e);
    }
  }

  async templateUploadAndRender(body) {
    try {
      const url = `${this.apiV2}/template/render`;
      log.debug(`POST to ${url}`, { function: 'templateUploadAndRender' });

      const { data, headers, status } = await this.axios.post(url, body, {
        responseType: 'arraybuffer' // Needed for binaries unless you want pain
      });

      return { data, headers, status };
    } catch (e) {
      errorToProblem(SERVICE, e);
    }
  }

  async templateRender(templateId, body) {
    try {
      const url = `${this.apiV2}/template/${templateId}/render`;
      log.debug(`POST to ${url}`, { function: 'templateRender' });

      const { data, headers, status } = await this.axios.post(url, body, {
        headers: {
          'content-type': 'application/json'
        },
        responseType: 'arraybuffer'
      });

      return { data, headers, status };
    } catch (e) {
      errorToProblem(SERVICE, e);
    }
  }

  async getTemplate(templateId) {
    try {
      const url = `${this.apiV2}/template/${templateId}`;
      log.debug(`GET to ${url}`, { function: 'getTemplate' });

      const { data, status } = await this.axios.get(url, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      return { data, status };
    } catch (e) {
      if (e.response && e.response.status === 404) {
        return { data: 'Not Found', status: 404 };
      }
      errorToProblem(SERVICE, e);
    }
  }

  async uploadTemplate(path) {
    try {
      const form = new FormData();
      form.append('template', fs.createReadStream(path));

      const url = `${this.apiV2}/template`;
      log.debug(`POST to ${url}`, { function: 'uploadTemplate' });

      const { data, headers, status } = await this.axios(
        {
          method: 'post',
          url: url,
          data: form,
          headers: {
            'content-type': `multipart/form-data; boundary=${form._boundary}`,
          },
        }
      );

      return { data, headers, status };
    } catch (e) {
      errorToProblem(SERVICE, e);
    }
  }

  async getHash(file) {
    const hash = crypto.createHash('sha256');
    const stream = fs.createReadStream(file);
    return new Promise((resolve, reject) => {
      stream.on('readable', () => {
        let chunk;
        while (null !== (chunk = stream.read())) {
          hash.update(chunk);
        }
      });
      stream.on('end', () => resolve(hash.digest('hex')));
      stream.on('error', error => reject(error));
    });
  }


}

const endpoint = config.get('serviceClient.commonServices.cdogs.endpoint');
const tokenEndpoint = config.get('serviceClient.commonServices.tokenEndpoint');
const username = config.get('serviceClient.commonServices.username');
const password = config.get('serviceClient.commonServices.password');

let cdogsService = new CdogsService({tokenUrl: tokenEndpoint, clientId: username, clientSecret: password, apiUrl: endpoint});
module.exports = cdogsService;
