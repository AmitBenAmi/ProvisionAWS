FROM node:current-alpine3.11

RUN mkdir /home/node/app && chown -R node:node /home/node/app && \
    mkdir /home/node/app/secrets && chown -R node:node /home/node/app/secrets

WORKDIR /home/node/app
COPY ["package.json", "index.js", "./"]
COPY ["key.pem", "cert.pem", "./secrets/"]

USER node
RUN npm install

ENV WEB_PORT 8080
ENV SSL_CERTIFICATES_PATH ./secrets
ENTRYPOINT [ "node", "index.js" ]