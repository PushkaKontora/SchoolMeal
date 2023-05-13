CHILDREN_PREFIX = "/child"


def child_prefix(child_id: str) -> str:
    return CHILDREN_PREFIX + f"/{child_id}"
