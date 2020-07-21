# Deploying To Openshift

## Post-Deployment Tweaks

Some of the deployments will require additional tweaks after the first deployment has been generated. In particular:

### Controller

The database connection strings set by the following environment variables will need to be updated with the user/password generated when deploying the database:

- IdentityServer__ConnectionStrings__Database
- UrlShortenerService__ConnectionStrings__Database
- SessionStorageService__ConnectionStrings_Database

# Agent

The `WEBHOOK_URL` environment variable will need to be updated to use the controller's API key. This is achieved by adding `/my-controller-api-key` to the existing value.

Additionally, the agent will need to be registered on the ledger, as it cannot perform this task automatically. To do this, determine which ledger the agent will be connected to (e.g.: by inspecting the `GENESIS_URL` agent environment variable) and register the agent using the seed stored in the agent's wallet secret in OpenShift.
