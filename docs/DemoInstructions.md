# VC Authentication OIDC (vc-authn-oidc): Demo Deployment

If you are interested in trying out using a verifiable credential in an Open ID Connect (OIDC) interaction to receive authorization to access a service, follow the steps below. Following the instructions is a link to a presentation that provides some insight into the authorization flow.

The premise of the demo is that you first get a verifiable credential from an appropriate authority, and then you use that credential to get access to a protected resource. In this case, a sufficient authority is a service that makes you prove control over your email address, while the protected service is a mock BC Government website.

## Get a compatible mobile agent

The demo supports the identity agent app from [Streetcred.id](https://Streetcred.id) for iOS and Android. There is some setup special setup needed for the Streetcred agent. Please follow the instructions [here](https://github.com/bcgov/identity-kit-poc/blob/master/docs/GettingApp.md) to setup the agent and then return back here for the rest of the instructions.

**Are you a mobile agent builder?**  We'd love to work with you to get your implementation working with the [vc-authn-oidc](https://github.com/bcgov/vc-authn-oidc) identity provider. If you are testing with our deployed service and have questions, please contact us on the #aries channel on [Hyperledger Rocketchat](https://chat.hyperledger.org) (you will need a free [Linux Foundation account](https://identity.linuxfoundation.org/user) to access that channel), or email us [here](mailto:swcurran@cloudcompass.ca).

## Get a verifiable email credential

To get your verified email credential, go to this [email verification service](https://email-verification.vonx.io/) run by the Province of BC. Enter your email address, check your email for an message from the service, and follow the instructions to get your verified email address credential.

If you want, you can use your verified email credential to get an IIWBook credential that can also be used for authorization in the next step. Interested? Follow the instructions [here](https://iiwbook.vonx.io).

## Use the Verifiable Credential Identity Provider

With the necessary verified credential(s) in hand, you are ready to access the protected resources&mdash;the mock BC Government service ("Access to Audio"). Go to the [service](https://verified-email-authentication.pathfinder.gov.bc.ca), and click on the "Proceed" button to authenticate. You will see a QR code that your mobile agent should be able to process. Assuming you have your verified email credential already, the mobile agent will help you present your credentials and you will be granted access to the service.

If you are an OIDC IAM provider, or you have an IAM deployment with any standard OIDC implementation (e.g. [Keyclock](https://www.keycloak.org/), [Gluu](https://www.gluu.org/), [Forge Rock](https://www.forgerock.com/), etc.) and would like to add verifiable credential-based authorization, let us know. We'd be glad to work with you to get this demonstration setup on your site, including how you can issue your own credentials to your users.

## About the Flow

This [presentation](https://docs.google.com/presentation/d/150n2PikoshbQB46QDMO3xpWFVLdcsoJNey0MVtCbGvk/edit?usp=sharing) provides some details about the vc-authn-oidc implementation, including assumptions about the setup and the message flow from QR code to authorization being granted. Take a look and let us know if you have any questions.

Looking for even more technical details? See the [README](README.md) in this repo for all the technical details of this implementation, and guidance on how you can deploy it.