[![img](https://img.shields.io/badge/Lifecycle-Maturing-007EC6)](https://github.com/bcgov/repomountie/blob/master/doc/lifecycle-badges.md)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

[![unit-tests](https://github.com/bcgov/vc-authn-oidc/actions/workflows/controller_unittests.yml/badge.svg?branch=2.0-development&event=push)](https://github.com/bcgov/vc-authn-oidc/actions/workflows/controller_unittests.yml)

# Verifiable Credential Authentication with OpenID Connect (VC-AuthN OIDC)

Verifiable Credential Identity Provider for OpenID Connect.

See [here](/docs/README.md) for background into how this integration is defined.

For configuration instructions, refer to the [configuration guide](/docs/ConfigurationGuide.md).

Make sure to read the [best practices](/docs/BestPractices.md) to be used when protecting a web application using `vc-authn-oidc`.

## Pre-requisites

- A bash-compatible shell such as [Git Bash](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/get-docker/)
- Ngrok token (optional, required for local development)

## Configuring Ngrok

Each developer must apply for an Ngrok token [here](https://dashboard.ngrok.com/get-started/your-authtoken). Then place the token into the .env-dev file within the docker directory.

```
NGROK_AUTHTOKEN=<your token here>
```

## Running VC-AuthN

Open a shell in the [docker](docker/) folder and run the following commands:

- `./manage build`: this command will build the controller image. This step is required the first time the project is run, and when dependencies in change in the requirements file(s).
- `./manage start`: this will start the project. The user will be prompted to select whether to target the default standalone ACA-Py agent, or a tenant on a pre-provisioned instance of [Traction](https://github.com/bcgov/traction). Follow the script prompts to select the appropriate runtime options: they will be saved in an `env` file for the next execution.
- To reset everything (including removing container data and selected options in the `env` file) execute `./manage rm`.

A list of all available commands is visible by executing `./manage -h`.

The project is set-up to run without needing any external dependencies by default, using a standalone agent in read-only that will target the ledgers specified in [ledgers.yaml](docker/agent/config/ledgers.yaml).

If a [Traction](https://github.com/bcgov/traction) tenant is selected via user prompts for the agent, some pre-requisite steps are required for the project to start-up successfully:

- clone the [Traction](https://github.com/bcgov/traction) repository.
- add the following to `<traction_folder>/scripts/docker-compose.yaml`

  ```yaml
  networks:
    default:
      name: oidc_vc_auth
      external: true
  ```
- copy `scripts/.env-example` to `scripts/.env` and adjust as necessary, for more info see [run local traction.](https://github.com/bcgov/traction/blob/main/scripts/README.md#run-local-traction)
- start `traction` by executing `docker-compose up` from `<traction_folder>/scripts`
- provision yourself a tenant and record the wallet Id/Key: they will be required to connect the controller with the agent.

## Using VC-AuthN

To use VC-AuthN for development and/or demo purposes, a pre-configured demo app is provided in the [demo/vue](demo/vue/) folder. To start it, execute `docker compose up` from within the `demo/vue` folder.

In order to use the VC OIDC authentication, a couple of extra steps are required:

- A proof-request configuration needs to be registered with VC-AuthN. To do
  so, the following command can be used to post a configuration requesting a BCGov Verified Email credential:

```bash
curl -X 'POST' \
  'http://localhost:5000/ver_configs/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "ver_config_id": "verified-email",
  "subject_identifier": "email",
  "proof_request": {
    "name": "BCGov Verified Email",
    "version": "1.0",
    "requested_attributes": [

      {
        "names": ["email"],
        "restrictions": [
          {
            "schema_name": "verified-email",
            "issuer_did": "MTYqmTBoLT7KLP5RNfgK3b"
          }
        ]
      }
    ],
    "requested_predicates": []
  }
}'
```

- The demo application is configured to use Keycloak as AIM system. To register keycloak as a client for VC-AuthN, execute the following command in a shell:

```bash
curl -X 'POST' \
  'http://localhost:5000/clients/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "client_id": "keycloak",
  "client_name": "keycloak",
  "client_secret": "**********",
  "response_types": [
    "code",
    "id_token",
    "token"
  ],
  "token_endpoint_auth_method": "client_secret_basic",
  "redirect_uris": [
    "http://localhost:8880/auth/realms/vc-authn/broker/vc-authn/endpoint"
  ]
}'
```

- Lastly, obtain a valid BCGov Verified Email credential from the [BCGov Email Verification Service](https://email-verification.vonx.io)

After all these steps have been completed, you should be able to authenticate with the demo application using the "Verified Credential Access" option.

## Debugging

To connect a debugger to the `vc-authn` controller service, start the project using `DEBUGGER=true ./manage start` and then launch the debugger, it should connect automatically to the container.

This is a sample debugger launch configuration for VSCode that can be used by adding it to `launch.json`:
```json
{
    "version": "0.1.0",
    "configurations": [
        {
            "name": "Python: Debug VC-AuthN Controller",
            "type": "python",
            "request": "attach",
            "port": 5678,
            "host": "localhost",
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/oidc-controller",
                    "remoteRoot": "/app"
                }
            ]
        }
    ]
}
```