// Jest 25.x onwards emits coverage reports on a different source path
// https://stackoverflow.com/q/60323177
const fs = require('fs');
const file = './coverage/lcov.info';

fs.readFile(file, 'utf8', (err, data) => {
  if (err) {
    return console.error(err); // eslint-disable-line no-console
  }
  const result = data.replace(/src/g, `${process.cwd()}/src`);

  fs.writeFile(file, result, 'utf8', err => {
    if (err) return console.error(err); // eslint-disable-line no-console
  });
});
