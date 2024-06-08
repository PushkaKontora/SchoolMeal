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

RUN echo "export const BASE_BACKEND_URL = 'https://$API_DOMAIN/api';" > $WORK_DIR/src/7_shared/api/implementations/basic/config.ts

RUN npm run lint

RUN npm run build


FROM nginx:1.23.4-alpine3.17 as proxy

ARG TEMPLATE_DIR=/etc/nginx/templates
ARG CONFIG_DIR=/etc/nginx/conf.d

ENV NGINX_ENVSUBST_TEMPLATE_DIR $TEMPLATE_DIR
ENV NGINX_ENVSUBST_OUTPUT_DIR $CONFIG_DIR

RUN mkdir $TEMPLATE_DIR
COPY nginx/default.conf.template $TEMPLATE_DIR

EXPOSE 80
USER $USER


FROM proxy

COPY --from=build /web/dist /usr/share/nginx/html