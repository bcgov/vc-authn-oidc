# Special Instructions for Play With Docker

These instructions guide you through running this demo in [Play with Docker](https://labs.play-with-docker.com/). Not familiar with Play with Docker?  Read [this](https://github.com/cloudcompass/ToIPLabs/blob/master/docs/LFS173x/RunningLabs.md#running-on-play-with-docker) for information about Play with Docker and how to use it.

To run the demo, start up a Play with Docker terminal session and run the following commands. Copying and pasting (right-click Paste) into the terminal session is easiest.

```bash
git clone https://github.com/bcgov/vc-authn-oidc
cd vc-authn-oidc
cd demo
./PWDrun

```

The last of those commands invokes a script that:

- Builds and deploys the verifiable credential Identity Provider (IdP).
- Registers an authentication presentation request that requires proof of having a verified email verifiable credential from the [BC Gov Verified Email service](https://email-verification.vonx.io/).
- Builds and deploys the (demo) website that is protected by the IdP.

Once everything is running, click on the port at the top of the screen labelled `8080` to go to the demo website. If you are quick, you may see a `502 Bad Gateway` error because the website isn't initialized yet. Hitting refresh should get you the website. If you don't see the `8080` link, you can click `Open Port` and enter `8080` when prompted.

Once you are on the website, click the `Authenticate` link. The IdP is invoked and you are asked to scan a QR code, or click a link to receive the presentation request so that you can present your proof. Once done, you will be granted access to the site. And that's it!

If you want, in the `demo` folder (same as the script that runs everything) is a file `presentationRequest.json`. You can edit that to change the presentation request to anything you want. This is a good way to test presentation requests. On Play with Docker you can use either `vi` or a GUI editor (click `Editor` in the header and enlarge the resulting window) to edit the file. Once you have updated the Presentation Request you can run:

```bash
./updatePresentation presentationRequest.json

```

> NOTE: If you change the `id` of the presentation request, you must add a `--new` parameter between the command and file names.

Once you are finished with the demo you can just close the Play with Docker session. If you want to stop and restart the demo, then you can use the command from the terminal command line:

```bash
./PWDdown

```
