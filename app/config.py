import os
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    MONGO_USER: str
    MONGO_PW: str
    MONGO_DB_STRING: str
    AZURE_OPENAI_KEY: str
    AZURE_OPENAI_DEPLOYMENT: str
    AZURE_OPENAI_ENDPOINT: str
    APIFY_API_KEY: str
    COMMENTS_PER_POST: int
    POSTS_PER_PROFILE: int
    REPLICATE_API_TOKEN: str
    ENV: str
    
    class Config:
        env_file = ".env"

# Create the config object
consts = Config()

# Access your variables through this config object, for example:
# db_uri = config.MONGO_DB_STRING