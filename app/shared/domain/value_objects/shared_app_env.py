from dataclasses import dataclass
from enum import Enum
from os import getenv


class Environments(str, Enum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"
    DEBUG = "debug"


@dataclass(frozen=True)
class SharedAppEnv:
    value: str = getenv("APP_ENV", Environments.PROD.value)

    def __post_init__(self):
        if self.value != Environments.DEV or self.value != Environments.TEST or self.value != Environments.PROD:
            raise ValueError(f"Invalid environment {self.value}")

    @classmethod
    def isTest(cls) -> bool:
        return cls.value == Environments.TEST

    @classmethod
    def isDev(cls) -> bool:
        return cls.value == Environments.DEV

    @classmethod
    def isProd(cls) -> bool:
        return cls.value == Environments.PROD

    @classmethod
    def isDebug(cls) -> bool:
        return cls.value == Environments.DEBUG
