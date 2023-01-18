const Problem = require('api-problem');

const log = require('./log')(module.filename);

module.exports = function(service, e) {
  if (e.response) {
    // Handle raw data
    let data;
    if (typeof e.response.data === 'string' || e.response.data instanceof String) {
      data = JSON.parse(e.response.data);
    } else {
      data = e.response.data;
    }

    log.error(`Error from ${service}: status = ${e.response.status}, data : ${JSON.stringify(data)}`);
    // Validation Error
    if (e.response.status === 422) {
      throw new Problem(e.response.status, {
        detail: data.detail,
        errors: data.errors
      });
    }
    // Something else happened but there's a response
    throw new Problem(e.response.status, { detail: e.response.data.toString() });
  } else {
    log.error(`Unknown error calling ${service}: ${e.message}`);
    throw new Problem(502, `Unknown ${service} Error`, { detail: e.message });
  }
};
