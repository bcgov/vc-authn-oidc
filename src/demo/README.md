## Prepare
### Run docker-compose
`docker-compose -f docker-compose.yml up -d`

   It'll start:
   - Postgres db for the VCAuthn service
   - Keycloak with a pre-configured vc-authn realm

### Start VCAuthn service
`dotnet run`

### Seed Presentation configuration
```
POST https://localhost:5001/api/vc-configs
Content-Type: application/json

{
    "id" : "test",
    "subject_identifier" : "attribute1",
    "configuration" : {
        "name" : "test",
        "version" : 1.0,
        "requested_attributes" : {
            "attribute1": {
                "name" : "attribute1",
                "restrictions" : [
                    {
                        "schema_id": "123",
                        "schema_issuer_did": "",
                        "schema_name": "name",
                        "schema_version": "",
                        "issuer_did": "",
                        "cred_def_id": "",
                    }
				]
            },
            "attribute2": {
                "name" : "attribute2",
                "restrictions" : [
                    {
                        "schema_id": "345",
                        "schema_issuer_did": "",
                        "schema_name": "name",
                        "schema_version": "",
                        "issuer_did": "",
                        "cred_def_id": "",
                    }
				]
            }
		}
    }
}
```

## Test
### Start Workflow
Open  
`http://localhost:8180/auth/realms/vc-authn/protocol/openid-connect/auth?client_id=security-admin-console&redirect_uri=http%3A%2F%2Flocalhost%3A8180%2Fauth%2Fadmin%2Fmaster%2Fconsole%2F%23%2Frealms%2Fvc-authn%2Fidentity-provider-settings&state=f0bfe2a2-a9b3-42dc-a84b-cb50e88055eb&response_mode=fragment&response_type=code&scope=openid&nonce=c93d4634-e6fc-45d8-8a4c-bc9a28db56dc&pres_req_conf_id=test`

and click `oidc` option