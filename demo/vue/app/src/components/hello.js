const log = require('./log')(module.filename);

const hello = {
  /**
   * @function getHello
   * Returns hello world
   * @returns {string} A string
   */
  getHello: () => {
    const value = 'Hello World!';
    log.info(value, { function: 'getHello' });
    return value;
  }
};

module.exports = hello;
