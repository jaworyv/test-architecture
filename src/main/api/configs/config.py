from pathlib import Path
from typing import Any
import os

class Config:
    _instance = None
    _dictionary = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)

            config_path = Path(__file__).parents[4] / "resources" / "urls.properties"

            if not config_path.exists():
                raise FileNotFoundError(f"Config path not found {config_path}")

            with open(config_path, "r") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.split("=")
                        cls._dictionary[key] = value.strip()

        return cls._instance

    @staticmethod
    def fetch(key: str, default_value: Any = None) -> Any:
        config = Config()

        env_key = {
            "backendUrl": "BACKEND_URL",
            "dataBaseUrl": "DATABASE_URL",
        }.get(key)

        if env_key:
            env_value = os.getenv(env_key)

            if env_value is not None:
                return env_value

        return config._dictionary.get(key, default_value)