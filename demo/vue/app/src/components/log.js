const config = require('config');
const jwt = require('jsonwebtoken');
const { parse } = require('path');
const Transport = require('winston-transport');
const { createLogger, format, transports } = require('winston');
const { logger } = require('express-winston');

/**
 * Class representing a winston transport writing to null
 * @extends Transport
 */
class NullTransport extends Transport {
  /**
   * Constructor
   * @param {object} opts Winston Transport options
   */
  constructor(opts) {
    super(opts);
  }

  /**
   * The transport logger
   * @param {object} _info Object to log
   * @param {function} callback Callback function
   */
  log(_info, callback) {
    callback();
  }
}

/**
 * Main Winston Logger
 * @returns {object} Winston Logger
 */
const log = createLogger({
  exitOnError: false,
  format: format.combine(
    format.errors({ stack: true }), // Force errors to show stacktrace
    format.timestamp(), // Add ISO timestamp to each entry
    format.json(), // Force output to be in JSON format
  ),
  level: config.get('server.logLevel')
});

if (process.env.NODE_ENV !== 'test') {
  log.add(new transports.Console({ handleExceptions: true }));
} else {
  log.add(new NullTransport());
}

if (config.has('server.logFile')) {
  log.add(new transports.File({
    filename: config.get('server.logFile'),
    handleExceptions: true
  }));
}

/**
 * Returns a Winston Logger or Child Winston Logger
 * @param {string} [filename] Optional module filename path to annotate logs with
 * @returns {object} A child logger with appropriate metadata if `filename` is defined. Otherwise returns a standard logger.
 */
const getLogger = (filename) => {
  return filename ? log.child({ component: parse(filename).name }) : log;
};

/**
 * Returns an express-winston middleware function for http logging
 * @returns {function} An express-winston middleware function
 */
const httpLogger = logger({
  colorize: false,
  // Parses express information to insert into log output
  dynamicMeta: (req, res) => {
    const token = jwt.decode((req.get('authorization') || '').slice(7));
    return {
      azp: token && token.azp || undefined,
      contentLength: res.get('content-length'),
      httpVersion: req.httpVersion,
      ip: req.ip,
      method: req.method,
      path: req.path,
      query: Object.keys(req.query).length ? req.query : undefined,
      responseTime: res.responseTime,
      statusCode: res.statusCode,
      userAgent: req.get('user-agent')
    };
  },
  expressFormat: true, // Use express style message strings
  level: 'http',
  meta: true, // Must be true for dynamicMeta to execute
  metaField: null, // Set to null for all attributes to be at top level object
  requestWhitelist: [], // Suppress default value output
  responseWhitelist: [], // Suppress default value output
  // Skip logging kube-probe requests
  skip: (req) => req.get('user-agent') && req.get('user-agent').includes('kube-probe'),
  winstonInstance: log,
});

module.exports = getLogger;
module.exports.httpLogger = httpLogger;
module.exports.NullTransport = NullTransport;
