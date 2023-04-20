FROM alpine:3.16

WORKDIR /usr/bin

RUN wget -q https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-arm -O mkcert && \
    chmod +x mkcert

WORKDIR /cert

RUN mkcert -install && \
    mkcert -key-file key.pem -cert-file cert.pem localhost 127.0.0.1 ::1