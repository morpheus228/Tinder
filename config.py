from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass
class BotConfig:
    token: str
    link: str
    # admin_ids: list


@dataclass
class MirrorConfig:
    bot_link: str

@dataclass
class PostgresConfig:
    host: str
    password: str
    user: str
    database: str
    port: str


@dataclass
class Config:
    bot: BotConfig
    mirror: MirrorConfig
    postgres: PostgresConfig

    def __init__(self):
        load_dotenv('.env')
        
        self.bot = BotConfig(
            token=os.getenv("BOT_TOKEN"),
            link=os.getenv('BOT_LINK'))

        self.mirror = MirrorConfig(bot_link=os.getenv("MIRROR_BOT_LINK"))

        self.postgres = PostgresConfig(
            host=os.getenv('POSTGRES_HOST'),
            password=os.getenv('POSTGRES_PASSWORD'),
            user=os.getenv('POSTGRES_USER'),
            database=os.getenv('POSTGRES_DB'),
            port=os.getenv('POSTGRES_PORT'))