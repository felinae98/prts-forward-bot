from pydantic import BaseSettings

class Config(BaseSettings):

    weibo_id: str
    target_group: list[str]

    class Config:
        extra = "ignore"
