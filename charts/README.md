# Deploying vc-authn-oidc

Until an Aries Cloudagent Python helm chart is available to be used as dependency, the templates in the [openshift](../openshift/) folder should be used to deploy the agent component. This should be done *before* executing the charts that deploy `vc-authn` and remaining dependencies.

*Note:* the provided configurations are for OpenShift.

## Configuration
Use the `acapy` section in the chart to specify the settings for the target agent:

- `agentUrl`: this is the public URL for the agent (also known as endpoint)
- `adminUrl`: this is the URL to the admin interface of the agent - it will be used by `vc-authn-oidc` to control it
- `existingSecret`: the name of an existing secret containing the values for `x-api-key` (otherwise set using `adminApiKey`), `wallet-id` and `wallet-key` (otherwise set using `tenant.walletId` and `tenant.walletKey`). 
- `useOob`: values are `true` or `false` (default `false`). If set to `true`, use OOB rather than connection-less to generate a proof-request.
- `adminApiKey`: the value of the `x-api-key` header to be used when making requests to the aca-py instance
existingSecret: ""
- `tenancyMode`: valid options are `multi` and `single`. If `multi` is selected, the following `tenant` section must be completed as well.
- `tenant.walletId`: the wallet id to be used to authenticate with the Traction tenant.
- `tenant.walletKey`: the wallet key to be used to authenticate with the Traction tenant.