from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    ebay_app_id: str
    tcgplayer_public_key: str
    tcgplayer_private_key: str
    resend_api_key: str
    alert_email_to: str


settings = Settings() # type: ignore
