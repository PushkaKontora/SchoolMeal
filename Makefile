new_env:
	tools/generate_env.sh

certificate:
	docker run --rm -v ./certs:/root/.local/share/mkcert brunopadz/mkcert-docker \
		/bin/sh -c "cd /root/.local/share/mkcert/ && \
		mkcert -install && \
		mkcert -cert-file certificate.pem -key-file private.pem localhost 127.0.0.1 && \
		cat rootCA.pem >> certificate.pem"

test_db:
	docker-compose -f docker-compose.yaml -f docker-compose.test_db.yaml up --build test_db