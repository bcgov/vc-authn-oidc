# Vue Scaffold Application

This node.js scaffold app hosts the Vue scaffold frontend. It implements a minimal endpoint to allow for Keycloak authentication.

## Configuration

The Vue scaffold app will require some configuration. The API will be locked down and require a valid JWT Token to access. We will need to configure the application to authenticate using the same Keycloak realm as the [frontend](frontend). Note that the Vue scaffold frontend is currently designed to expect all associated resources to be relative to the original access path.

## Super Quickstart

In general, most of these npm run scripts can be prepended with `all:` in order to run the same operation on both the application and the frontend sequentially.

### Local Config Setup

Ensure that you have filled in all the appropriate configurations following [config/custom-environment-variables.json](config/custom-environment-variables.json) before proceeding.

The [config/custom-environment-variables.json](config/custom-environment-variables.json) file provides a complete mapping of ENV variables to the config that the node application will see, and the [config/default.json](config/default.json)default.json provides generic defaults for all non-sensitive config values. If you do a search for `config.get(...)` on the repository, you'll get a sense of how the configuration variables are utilized in this project.

If you are running this on a local machine, you will need to create a `local.json` file in the `config` directory containing the values you want set. For more information on how the config library loads and searches for environment variables, take a look at this article: <https://github.com/lorenwest/node-config/wiki/Configuration-Files>.

At an absolute bare minimum, we recommend that you will want your `local.json` to at least have the following values defined (replacing `REDACTED` with your own values as needed):

``` json
{
  "frontend": {
    "keycloak": {
      "clientId": "REDACTED",
      "realm": "REDACTED",
      "serverUrl": "REDACTED"
    }
  },
  "server": {
    "keycloak": {
      "clientId": "REDACTED",
      "clientSecret": "REDACTED",
      "realm": "REDACTED",
      "serverUrl": "REDACTED"
    },
    "logLevel": "debug",
    "morganFormat": "dev",
    "port": "8080"
  }
}
```

### Production Build and Run

``` sh
npm run all:fresh-start
```

### Development Run

``` sh
npm run serve
```

Start a new terminal

``` sh
cd frontend
npm run serve
```

### Run application tests

``` sh
npm run test
```

### Lints and fixes application files

``` sh
npm run lint
npm run lint-fix
```
