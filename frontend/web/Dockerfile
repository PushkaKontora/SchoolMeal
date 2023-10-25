FROM node:16.20.2-buster-slim as build

ARG WORK_DIR=/web
WORKDIR $WORK_DIR

ENV PATH=$WORK_DIR/node_modules/.bin:$PATH

COPY package.json $WORK_DIR
COPY package-lock.json $WORK_DIR
RUN npm ci --silent

COPY public $WORK_DIR/public
COPY tsconfig.json $WORK_DIR
COPY tsconfig.node.json $WORK_DIR
COPY .eslintrc.cjs $WORK_DIR

COPY store $WORK_DIR/store
COPY src $WORK_DIR/src

RUN npm run lint

RUN npm run build

FROM nginx:1.23.4-alpine3.17 as final

ARG CONFIG_DIR=/etc/nginx/conf.d

COPY nginx/default.conf $CONFIG_DIR
COPY nginx/upstream.conf $CONFIG_DIR
COPY --from=build /web/build /usr/share/nginx/html

EXPOSE 80
USER $USER