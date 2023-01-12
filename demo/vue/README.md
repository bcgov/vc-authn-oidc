
# Vue Keycloak Scaffold [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE) [![img](https://img.shields.io/badge/Lifecycle-Stable-97ca00)](https://github.com/bcgov/repomountie/blob/master/doc/lifecycle-badges.md)

![Tests](https://github.com/bcgov/vue-scaffold/workflows/Tests/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/e7f26d580793ba73b7f7/maintainability)](https://codeclimate.com/github/bcgov/vue-scaffold/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/e7f26d580793ba73b7f7/test_coverage)](https://codeclimate.com/github/bcgov/vue-scaffold/test_coverage)

A clean Vue Keycloak full-stack scaffold example

## Directory Structure

    .github/                   - PR and Issue templates
    app/                       - Application Root
    ├── frontend/              - Frontend Root
    │   ├── src/               - Vue.js frontend web application
    │   └── tests/             - Vue.js frontend web application tests
    ├── src/                   - Node.js backend web application
    │   └── docs/              - OpenAPI 3.0 Specification
    └── tests/                 - Node.js backend web application tests
    openshift/                 - OpenShift-deployment and shared pipeline files
    CODE-OF-CONDUCT.md         - Code of Conduct
    COMPLIANCE.yaml            - BCGov PIA/STRA compliance status
    CONTRIBUTING.md            - Contributing Guidelines
    Jenkinsfile                - Top-level Pipeline
    Jenkinsfile.cicd           - Pull-Request Pipeline
    LICENSE                    - License

## Documentation

* [Application Readme](app/README.md)
* [Frontend Readme](app/frontend/README.md)
* [Openshift Readme](openshift/README.md)
* [Devops Tools Setup](https://github.com/bcgov/nr-showcase-devops-tools)

## Quick Start Dev Guide

You can quickly run this application in production mode after cloning with the following commands (assuming you have already set up local configuration as well). Refer to the [Application Readme](app/README.md) and [Frontend Readme](app/frontend/README.md) for more details.

    cd app
    npm run all:install
    npm run all:build
    npm run serve

## Getting Help or Reporting an Issue

To report bugs/issues/features requests, please file an [issue](https://github.com/bcgov/vue-scaffold/issues).

## How to Contribute

If you would like to contribute, please see our [contributing](CONTRIBUTING.md) guidelines.

Please note that this project is released with a [Contributor Code of Conduct](CODE-OF-CONDUCT.md). By participating in this project you agree to abide by its terms.

## License

    Copyright 2020 Province of British Columbia

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

## Design Rationale

This is designed as a minimally viable full-stack application which self-hosts the Vue frontend and consumes its API endpoint. This was purposely designed with as few dependencies as possible with a minimal amount of opinionation on design.

The frontend and the application can be treated as separate projects. The frontend will build and emit files under the app/frontend/dist folder. This is picked up by the node application and hosted as is with minimal routing changes. Alternative static hosting solutions such as Caddy or nginx may also be considered.

### Application

The application is a simple express application, with some basic support for HTTP issue codes through the `api-problem` package. It uses express routers to construct and mount the subpaths of the application. The API endpoint is mounted on the `/api` path, while the frontend is mounted on the `/app` path.

#### Application Components

The application has the following component dependencies:

* api-problem
* compression
* config
* express
* js-yaml
* keycloak-connect
* morgan
* npmlog

#### Code Organization

The app splits itself into routes and components, where routes handle network traffic, and components handle business logic. The demo `/api/v1/hello` endpoint is an authenticated keycloak protected endpoint to demonstrate the use of the keycloak-connect middleware. Anything under the `/app` path will contain resources needed for the frontend to render on the browser.

### Frontend

The frontend was built up from scratch using the official [Vue CLI](https://cli.vuejs.org/) distribution. These were the options that were used when scaffolding the initial Frontend:

    Vue CLI v4.2.2
    ? Please pick a preset: Manually select features
    ? Check the features needed for your project: Babel, Router, CSS Pre-processors, Linter, Unit
    ? Use history mode for router? (Requires proper server setup for index fallback in production) No
    ? Pick a CSS pre-processor (PostCSS, Autoprefixer and CSS Modules are supported by default): Sass/SCSS (with node-sass)
    ? Pick a linter / formatter config: Prettier
    ? Pick additional lint features: (Press <space> to select, <a> to toggle all, <i> to invert selection)Lint on save
    ? Pick a unit testing solution: Jest
    ? Where do you prefer placing config for Babel, ESLint, etc.? In dedicated config files

We installed the Vuetify framework by running `vue add Vuetify` afterwards.

#### Frontend Components

The frontend has the following main component dependencies:

* @bcgov/bc-sans
* axios
* core-js
* keycloak-js
* nprogress
* vue
* vue-router
* vuetify
* vuex

#### Code Structure

For the most part, we follow the Vue CLI scaffold as it is presented. However, we do also include a Keycloak prototype, and a global base component design in order to facilitate better component reuse. Keycloak authentication is handled by the vue-keycloak-js package, and the minimal BCGov styles are componetized in order to stay out of the way of the application content as much as possible. The navigation bar leverages vue-router, and the router uses webpack lazy-loading in order to optimize network traffic. Any components that start with the name `Base` and are in the `app/frontend/src/components/base` folder will be globally mounted onto the Vue instance and will be usable anywhere.
