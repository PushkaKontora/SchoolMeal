import secrets
import string

import dotenv


SECRET_VARIABLES = ("JWT_SECRET",)
ENV_FILE = "env"


class SecretGenerator:
    _ALPHABET = string.ascii_letters + string.digits + "!@#%^&*(-_=+)"

    def __init__(self) -> None:
        self._generated_secrets: set[str] = set()

    def generate(self, length: int = 64) -> str:
        while True:
            secret = "".join(secrets.choice(self._ALPHABET) for _ in range(length))
            if not (secret.islower() or secret.isupper() or secret in self._generated_secrets):
                self._generated_secrets.add(secret)
                return secret


if __name__ == "__main__":
    gen = SecretGenerator()

    for key_var in SECRET_VARIABLES:
        dotenv.set_key(ENV_FILE, key_to_set=key_var, value_to_set=gen.generate(), quote_mode="never")
