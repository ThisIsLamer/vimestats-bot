FROM node:latest

RUN mkdir -p /home/node/node_apps/vimestats
WORKDIR /home/node/node_apps/vimestats

RUN npm i

COPY . ./
CMD ["npm", "run", "prod"]