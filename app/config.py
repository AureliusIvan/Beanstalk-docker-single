from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = "fastapi_user"
    POSTGRES_PASSWORD: str = "password123"
    POSTGRES_DB: str = "fastapi_db"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: str = "5432"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
