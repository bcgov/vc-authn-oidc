# ACAPy VC-AuthN Migration Guide

This document contains instructions and tips useful when upgrading ACAPy VC-AuthN.

## 1.x -> 2.x

The functionality has mostly remained unchanged, however there are some details that need to be accounted for.

* Endpoints: `authorization` and `token` endpoints have changed, review the new values by navigating to the `.well-known` URL and update your integration accordingly.

* Proof configurations: to be moved to a `v2.0` instance, the following changes need to happen in existing proof-configurations.
  - The `name` identifier for disclosed attributes has been deprecated, use the `names` array instead.
  - If backwards-compatibility with `v1.0` tokens is required, the `include_v1_attributes` flag should be switched to `true` (see the [configuration guide](./ConfigurationGuide.md)).

* Client Types: ACAPy VC-AuthN 2.0 currently only supports confidential clients using client id/secret. If public clients were previously registered, they will now need to use an AIM (e.g.: keycloak) as broker.
