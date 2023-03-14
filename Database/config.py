import json
from pathlib import Path
from typing import Optional


def get_secret(
    key: str,
    default_value: Optional[str] = None,
    json_path: str = str("secrets.json"),
):
    with open(json_path) as f:
        secrets = json.loads(f.read())
    try:
        return secrets[key]
    except KeyError:
        if default_value:
            return default_value
        raise EnvironmentError(f"Set the {key} environment variable.")


if __name__ == "__main__":
    DB_HOST = get_secret("DB_HOST")
    print(DB_HOST)