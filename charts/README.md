# Deploying `vc-authn-oidc`

Until an Aries Cloudagent Python helm chart is available to be used as dependency, the templates in the [openshift](../openshift/) folder should be used to deploy the agent component. This should be done *before* executing the charts that deploy `vc-authn` and remaining dependencies.

*Note:* the provided configurations are for OpenShift.
