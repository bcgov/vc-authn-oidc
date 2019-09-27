# Verifiable Credential Authentication with OpenID Connect (VC-AuthN OIDC)

This repository is the home of a project to achieve verifiable credential based authentication using OpenID Connect.

See [here](/docs/README.md) for background into how this integration is defined.

## Debug

The VCAuthn-Service has two main dependencies

1. A backend database, postgres is used as the provider
2. An instance of [ACA-Py](https://github.com/hyperledger/aries-cloudagent-python) for handling the interactions with verifiable credentials

To run the OIDC-Controller in debug, first you must run these dependencies with the following command

```
    docker-compose -f ./docker/docker-compose.local-debug.yml build
    docker-compose -f ./docker/docker-compose.local-debug.yml up
```

Following this you can either launch the VCAuthn-Service in debug via an IDE like VS Code or Visual Studio or run the following command

```
    dotnet run ./src/VCAuthn
```

## A Quick Demo

The following demo starts up the VCAuthn-Service and its associated dependencies, along with an instance of keycloak.

To start the demo run the following commands from within the `docker` folder:

```
    ./manage build
    ./manage start
```

Once you have the service running, a presentation request configuration must be configured on the service. You can configure this through either browsing to the swagger interface [here](http://localhost:5000) or running the following curl command with a valid request body

```
    curl -X POST "http://localhost:5000/api/vc-configs" -H "accept: application/json" -H "X-Api-Key: test" -H "Content-Type: application/json-patch+json" -d "{ \"id\": \"test\", \"subject_identifier\": \"email\", \"configuration\": { \"name\": \"Basic Proof\", \"version\": \"1.0\", \"requested_attributes\": [ { \"name\": \"email\", \"restrictions\": [] }, { \"name\": \"first_name\", \"restrictions\": [] }, { \"name\": \"last_name\", \"restrictions\": [] } ], \"requested_predicates\": [] }}"
```

> The API is protected with an APIKey which defaults to `Test` in the demo

An example of a valid presentation request configuration is the following.

```
{
  "id": "test",
  "subject_identifier": "email",
  "configuration": {
    "name": "Basic Proof",
    "version": "1.0",
    "requested_attributes": [
      {
        "name": "email",
        "restrictions": []
      },
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

After configuring this, if you used the above presentation request configuration example, you can browse to keycloaks login page with this [link](http://localhost:8180/auth/realms/vc-authn/protocol/openid-connect/auth?client_id=security-admin-console&redirect_uri=http%3A%2F%2Flocalhost%3A8180%2Fauth%2Fadmin%2Fmaster%2Fconsole%2F%23%2Frealms%2Fvc-authn%2Fidentity-provider-settings&state=f0bfe2a2-a9b3-42dc-a84b-cb50e88055eb&response_mode=fragment&response_type=code&scope=openid&nonce=c93d4634-e6fc-45d8-8a4c-bc9a28db56dc&pres_req_conf_id=test-request-config)

From here you can click the `vc-authn` option to try out the flow. Clicking this should redirect your browser to the VC-Authn service and display a QR-Code base challenge.

## Project Affiliation

This project was formed from the code with us [opportunity](https://www.bcdevexchange.org/opportunities/cwu/opp-create-a-red-hat-keycloak-identity-provider--idp--capable-of-processing-verifiable-credentials-using-decentralized-identity-technology-created-by-bc-gov-to-authorize-access-to-a-bc-government-digital-service-) executed by [Mattr](https://mattr.global) funded by [BCGov](https://www2.gov.bc.ca/).
