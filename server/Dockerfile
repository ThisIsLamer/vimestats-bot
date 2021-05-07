FROM node:latest

RUN groupadd --gid 3000 vimestats \
        && useradd --uid 3000 --gid vimestats --shell /bin/bash --create-home vimestats

USER vimestats

RUN mkdir -p /home/node/node_apps/vimestats
WORKDIR /home/node/node_apps/vimestats

RUN npm i

COPY . ./
CMD ["npm", "run", "prod"]