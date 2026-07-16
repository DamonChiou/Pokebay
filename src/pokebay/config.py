from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    ebay_app_id: str
    ebay_client_secret: str
    tcgplayer_public_key: str
    tcgplayer_private_key: str


settings = Settings() # type: ignore
