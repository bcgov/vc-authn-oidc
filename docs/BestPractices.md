# VC AuthN Best Practices

This document is intended as a list of best practices and recommendations that are applicable when using `vc-authn-oidc` as means of authorization provider for web applications.

## Ensure the response for the right proof was received

When using `vc-authn-oidc` to secure a web application, the request to the identity provider must include a `pres_req_conf_id` query parameter set to the id of the `vc-authn-oidc` configuration that must be used to authenticate with the Identity Provider.

The query parameter - however - can be changed dynamically: this is a desired behaviour, as it allows web applications to dynamically request the proof-request for the circumstance/scenario that is more appropriate.

Similarly to checking a user's roles, when an id token is received from vc-authn the application should check that the value of the `pres_req_conf_id` attribute on the id token matches the value of the query parameter submitted to the IdP in the first place. If this is not the case, the user authentication may have been successful, but it did not satisfy the initial requirements (another example could be a web application that allows authentication using multiple Identity Providers, but only one of those is authorized to provide extended privileges to the user).
