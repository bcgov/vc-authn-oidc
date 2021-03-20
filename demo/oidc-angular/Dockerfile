# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:12.8.1-alpine as build-stage

# Set environment
ARG configuration=production

RUN apk update && apk add --no-cache make git

# Install Angular CLI
RUN npm install @angular/cli@8.2.2 -g

# Change directory so that our commands run inside this new directory
WORKDIR /app

# Get all the code needed to run the app
COPY ./ /app/

# Install dependecies
RUN npm install


# Run the angular in product
RUN ng build --configuration=$configuration

# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx:1.15.8-alpine

# Remove default Nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy builded static web from build-stage into nginx
COPY --from=build-stage /app/dist/oidc-angular/ /usr/share/nginx/html

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD nginx -g "daemon off;"
