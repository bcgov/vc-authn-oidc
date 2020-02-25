# Special Instructions for Play With Docker

1. Install S2I using the following command: ```curl -L https://github.com/openshift/source-to-image/releases/download/v1.1.14/source-to-image-v1.1.14-874754de-linux-amd64.tar.gz | tar -xz -C /usr/local/bin```

2. Checkout repository: ```git clone https://github.com/bcgov/vc-authn-oidc.git && cd vc-authn-oidc```

3. Open ports 5679 (agent), 5000 (controller) and 8080 (demo app). Keep the tabs open as the URLs will be necessary to start the app.

4. Open the editor and replace `http://localhost:8080` at line 37 of [appsettings.json](../oidc-controller/src/VCAuthn/appsettings.json#L37) with the demo app URL obtained at step 3.

5. Build vc-authn by running the following command in the [docker](./docker) folder: ```./manage build```

6. Start vc-authn by running the following command in the [docker](./docker) folder: ```NGROK_AGENT_URL=... NGROK_CONTROLLER_URL=... ./manage start-demo```. Set the values for `NGROK_AGENT_URL` and `NGROK_CONTROLLER_URL` to the relevant URLs that were obtained at step 3.

7. Run the following command to add the appropriate configuration to vc-authn:```
curl -X POST "http://localhost:5000/api/vc-configs" -H "accept: application/json" -H "X-Api-Key: controller-api-key" -H "Content-Type: application/json-patch+json" -d "{\"id\": \"verified-email\",\"subject_identifier\": \"email\", \"configuration\": { \"name\": \"verified-email\", \"version\": \"1.0\", \"requested_attributes\": [ { \"name\": \"email\", \"restrictions\": [ { \"schema_name\": \"verified-email\", \"issuer_did\": \"MTYqmTBoLT7KLP5RNfgK3b\" } ] } ], \"requested_predicates\": [] }}"```

8. Build the demo app by running the following command in the [demo/docker](./demo/docker) folder: ```./manage build```

9. Start the demo app by running the following command in the [demo/docker](./demo/docker) folder: ```./manage start```
