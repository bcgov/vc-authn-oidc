# vc-authn-oidc

clone [traction](https://github.com/bcgov/traction)
connect those services to the network defined in by

adding the following to `<traction_folder>/scripts/docker-compose.yaml`

```
networks:
  default:
    external:
      name: oidc_vc_auth
```

`docker-compose up` from `<traction_folder>/scripts`

run `docker-compose up` from `demo/vue` of this project
run `./manage build` from `/docker` of this project to create and tag the image

*inspect `./manage` file for environment variables, commenting/un-commenting configuration for an external multi-tenanted acapy, or using the single-tenant acapy defined in `../docker/docker-compose.yaml`

run `./manage start-no-acapy` from `/docker` of this project

### Prepare Acapy wallet for use

have python installed. TODO, replace with this with BASH script.
run `pip install requests` if needed.
run `python wallet_init.py` from `/docker`

### Prepare controller for use

1. create default verification_configuration @`http://localhost:5201/docs#/ver_configs/create_ver_conf_ver_configs_post` execute that endpoint with default payload

### Prepare example wallet

You will need a digital wallet app with a credential that contains two attributes `first_name` and `last_name`

# MongoDB
Use `Block Storage` as pvc type for mongo when deployed on openshift.