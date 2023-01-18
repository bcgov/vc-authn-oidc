const helloRouter = require('express').Router();

const helloComponent = require('../../components/hello');

/** Returns hello world result */
// eslint-disable-next-line no-unused-vars
helloRouter.get('/', (_req, res, _next) => {
  const result = helloComponent.getHello();
  res.status(200).json(result);
});

module.exports = helloRouter;
