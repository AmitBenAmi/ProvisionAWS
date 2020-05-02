FROM node:current-alpine3.11

RUN mkdir /home/node/app && chown -R node:node /home/node/app

WORKDIR /home/node/app
COPY ["package.json", "index.js"] .

USER node
RUN npm install

ENTRYPOINT [ "node", "index.js" ]