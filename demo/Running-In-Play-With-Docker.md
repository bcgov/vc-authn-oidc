# Special Instructions for Play With Docker

These instructions guide you through running this demo in [Play with Docker](https://labs.play-with-docker.com/). Not familiar with Play with Docker?  Read [this](https://github.com/cloudcompass/ToIPLabs/blob/master/docs/LFS173x/RunningLabs.md#running-on-play-with-docker) for information about Play with Docker and how to use it.

To run the demo, start up a Play with Docker terminal session, highlight and copy the script below, and then paste it (right-click, paste) it into the terminal session.

> Note: There is a second script below to bring the docker containers down so you can rerun the process.

```
#!/bin/bash

# set -x

if [ $PWD_HOST_FQDN == "labs.play-with-docker.com" ]
    then
        export ETH_CONFIG="eth1"
    elif [ $PWD_HOST_FQDN == "play-with-docker.vonx.io" ]
    then
        export ETH_CONFIG="eth0"
    else
        export ETH_CONFIG="eth0"
fi
myhost=`ifconfig ${ETH_CONFIG} | grep inet | cut -d':' -f2 | cut -d' ' -f1 | sed 's/\./\-/g'`
export DEMO_APP_URL="http://ip${myhost}-${SESSION_ID}-8080.direct.${PWD_HOST_FQDN}"
export NGROK_AGENT_URL="http://ip${myhost}-${SESSION_ID}-5679.direct.${PWD_HOST_FQDN}"
export NGROK_CONTROLLER_URL="http://ip${myhost}-${SESSION_ID}-5000.direct.${PWD_HOST_FQDN}"

echo Get S2I

curl -L https://github.com/openshift/source-to-image/releases/download/v1.2.0/source-to-image-v1.2.0-2a579ecd-linux-amd64.tar.gz | tar -xz -C /usr/local/bin

echo Clone repo

git clone https://github.com/bcgov/vc-authn-oidc.git && cd vc-authn-oidc

echo Update appsettings.json

sed -i "37,37s#http://localhost:8080#${DEMO_APP_URL}#" oidc-controller/src/VCAuthn/appsettings.json

echo Verify update to appsettings file
git diff

echo Build vc-authn
cd docker
./manage build

echo Deploy vc-authn
./manage start-demo

export CONTROLLER_WAIT=10
echo Wait ${CONTROLLER_WAIT} seconds for the controller to be initialized
sleep ${CONTROLLER_WAIT}

echo Loop: Configure the VC IdP presentation request
until curl -X POST "http://localhost:5000/api/vc-configs" -H "accept: application/json"\
     -H "X-Api-Key: controller-api-key"\
     -H "Content-Type: application/json-patch+json"\
     -d "{\"id\": \"verified-email\",\
          \"subject_identifier\": \"email\",\
          \"configuration\": { \
                \"name\": \"verified-email\",\
                \"version\": \"1.0\",\
                \"requested_attributes\": [ { \
                     \"name\": \"email\",\
                     \"restrictions\": [ { \
                          \"schema_name\": \"verified-email\",\
                          \"issuer_did\": \"MTYqmTBoLT7KLP5RNfgK3b\" } ]\
                     } ],\
                     \"requested_predicates\": []\
                }\
            }"
do
  sleep ${CONTROLLER_WAIT}
done

echo Build demo app
cd ../demo/docker
./manage build

echo Deploy demo app
./manage start

echo Check what docker containers are running
docker ps

cd ~

echo Done!

```

Here is a script to bring the process down after completing the test:

```
#/bin/bash

cd ~
cd vc-authn-oidc/docker
./manage down
cd ../demo/docker
./manage down
cd ~

echo Down!

```
