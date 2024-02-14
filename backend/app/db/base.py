from typing import Any


class DictMixin:
    def dict(self) -> dict[str, Any]:
        excl = ("_sa_adapter", "_sa_instance_state")
        return {k: v for k, v in vars(self).items() if not k.startswith("_") and not any(hasattr(v, a) for a in excl)}
