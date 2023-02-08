[![img](https://img.shields.io/badge/Lifecycle-Maturing-007EC6)](https://github.com/bcgov/repomountie/blob/master/doc/lifecycle-badges.md)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

# Verifiable Credential Authentication with OpenID Connect (VC-AuthN OIDC)

Verifiable Credential Identity Provider for OpenID Connect.

See [here](/docs/README.md) for background into how this integration is defined.

For configuration instructions, refer to the [configuration guide](/docs/ConfigurationGuide.md).

Make sure to read the [best practices](/docs/BestPractices.md) to be used when protecting a web application using `vc-authn-oidc`.

# Pre-requisites

## Tooling

- A bash-compatible shell such as [Git Bash](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/get-docker/)

## Project Dependencies

To run `vc-authn` locally, you will need an instance of [von-network](https://github.com/bcgov/von-network) running in Docker. A different ledger can be targeted by setting the `LEDGER_URL` environment variable before starting the project.

It is possible to run the project targeting a multi-tenant ACA-Py instance managed by [traction](https://github.com/bcgov/traction). To use this option, prepare a `traction` instance by cloning the repository and performing these tasks:

- add the following to `<traction_folder>/scripts/docker-compose.yaml`

```yaml
networks:
  default:
    external:
      name: oidc_vc_auth
```

- start `traction` by executing `docker-compose up` from `<traction_folder>/scripts`

# Running VC-AuthN

Once the pre-requisites are met, open a shell in the [docker](./docker/) folder and run the following commands:

- `./manage build` to build the required service images
- `./manage start` to run the services

Follow the script prompts to select the appropriate runtime options: they will be saved in an `env` for the next execution.

To reset everything (including removing container data) execute `./manage rm`.

A list of all available commands is visible by executing `./manage -h`.

## Configuring a proof-request

To configure the default pre-built proof request, once the controller service is running execute `./manage configure-proof default` in a shell.
This will create the following configuration:

```json
{
  "ver_config_id": "test-request-config",
  "subject_identifier": "first_name",
  "proof_request": {
    "name": "Basic Proof",
    "version": "1.0",
    "requested_attributes": [
      {
        "name": "first_name",
        "restrictions": []
      },
      {
        "name": "last_name",
        "restrictions": []
      }
    ],
    "requested_predicates": []
  }
}
```

To add more proof-request configurations, use the following controller endpoint `http://localhost:5201/docs#/ver_configs/create_ver_conf_ver_configs_post`.
