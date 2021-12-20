[![img](https://img.shields.io/badge/Lifecycle-Maturing-007EC6)](https://github.com/bcgov/repomountie/blob/master/doc/lifecycle-badges.md)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

# Verifiable Credential Authentication with OpenID Connect (VC-AuthN OIDC)

This repository is the home of a project to achieve verifiable credential based authentication using OpenID Connect.

See [here](/docs/README.md) for background into how this integration is defined.

For configuration instructions, refer to the [configuration guide](/docs/ConfigurationGuide.md).

Make sure to read the [best practices](/docs/BestPractices.md) to be used when protecting a web application using `vc-authn-oidc`.

## A Quick Demo

### Pre-requisites
You will need an instance of [von-network](https://github.com/bcgov/von-network) running in Docker

### Running the demo

The following demo starts up the VCAuthn-Service and its associated dependencies, along with an instance of keycloak.

To start the demo run the following commands from within the `docker` folder:

```
    ./manage build
    ./manage start
```

Once you have the service running, a presentation request configuration must be configured on the service. You can configure this through either browsing to the swagger interface [here](http://localhost:5001) or running the following curl command with a valid request body

```
    curl -X POST "http://localhost:5001/api/vc-configs" -H "accept: application/json" -H "X-Api-Key: controller-api-key" -H "Content-Type: application/json-patch+json" -d "{ \"id\": \"test-request-config\", \"subject_identifier\": \"email\", \"configuration\": { \"name\": \"Basic Proof\", \"version\": \"1.0\", \"requested_attributes\": [ { \"name\": \"email\", \"restrictions\": [] }, { \"name\": \"first_name\", \"restrictions\": [] }, { \"name\": \"last_name\", \"restrictions\": [] } ], \"requested_predicates\": [] }}"
```

> The API is protected with an APIKey which defaults to `Test` in the demo

An example of a valid presentation request configuration is the following.

```
{
  "id": "test-request-config",
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

After configuring this, if you used the above presentation request configuration example, you can browse to keycloaks login page with this [link](http://localhost:5001/vc/connect/authorize?scope=openid+vc_authn&state=EI3kI8RFbpuIqZE_MEI0xsv18NjQOS1lkbrBtj3x2CE.wOX0F5IZd74.security-admin-console&response_type=code&client_id=keycloak&redirect_uri=http%3A%2F%2Flocalhost%3A8180%2Fauth%2Frealms%2Fvc-authn%2Fbroker%2Fvc-authn%2Fendpoint&nonce=eEJ7joxB5CC8j_LaOaw3Dg&pres_req_conf_id=test-request-config)

From here you can click the `vc-authn` option to try out the flow. Clicking this should redirect your browser to the VC-Authn service and display a QR-Code base challenge.

For more interactive demos, refer to the [demo readme](demo/README.md)

## Project Affiliation

This project was formed from the code with us [opportunity](https://www.bcdevexchange.org/opportunities/cwu/opp-create-a-red-hat-keycloak-identity-provider--idp--capable-of-processing-verifiable-credentials-using-decentralized-identity-technology-created-by-bc-gov-to-authorize-access-to-a-bc-government-digital-service-) executed by [Mattr](https://mattr.global) funded by [BCGov](https://www2.gov.bc.ca/).
