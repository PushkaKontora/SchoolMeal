env:
	tools/generate_env.sh

certs:
	DOMAIN=localhost; \
	SSL_DIR=env/nginx/certs; \
	mkdir -p $$SSL_DIR; \
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
		-keyout $$SSL_DIR/nginx.key -out $$SSL_DIR/nginx.crt \
		-subj "/C=RU/CN=$$DOMAIN/O=None"