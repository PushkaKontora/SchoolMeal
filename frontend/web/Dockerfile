FROM node:16.20.2-buster-slim as build

ARG WORK_DIR=/web
ARG API_DOMAIN
WORKDIR $WORK_DIR

ENV PATH=$WORK_DIR/node_modules/.bin:$PATH

COPY package.json $WORK_DIR
COPY package-lock.json $WORK_DIR
RUN npm ci --silent

COPY public $WORK_DIR/public
COPY tsconfig.json $WORK_DIR
COPY tsconfig.node.json $WORK_DIR
COPY .eslintrc.cjs $WORK_DIR
COPY index.html $WORK_DIR

COPY store $WORK_DIR/store
COPY src $WORK_DIR/src

COPY configure_api.sh $WORK_DIR
RUN chmod +x $WORK_DIR/configure_api.sh && \
    $WORK_DIR/configure_api.sh ./src/7_shared/api/config.ts

RUN npm run lint

RUN npm run build


FROM nginx:1.23.4-alpine3.17 as proxy

ARG CONFIG_DIR=/etc/nginx/conf.d

COPY nginx/default.conf $CONFIG_DIR
COPY nginx/upstream.conf $CONFIG_DIR

EXPOSE 80
USER $USER


FROM proxy as web

COPY --from=build /web/dist /usr/share/nginx/html