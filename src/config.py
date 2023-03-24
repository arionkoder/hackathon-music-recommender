from pydantic import BaseSettings


class Settings(BaseSettings):
    spotipy_client_id: str
    spotipy_client_secret: str
    openai_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
