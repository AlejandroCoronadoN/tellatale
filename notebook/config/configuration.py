"""Settings and configuration for the Reece Chat application."""
import os

from pydantic_settings import BaseSettings


class StartupSettings(BaseSettings):
    """A class representing the configuration settings for the application.

    Attributes:
        env_file (str): The path to the environment file used to load configuration settings.
        app_name (str): The name of the application.
        log_level (str): The logging level for the application.
        openai_api_key (str): The API key for OpenAI.

    """

    class Config:  # noqa: D106
        import os

        env_file = os.path.join(os.path.dirname(__file__), "dev.env")

SETTINGS = StartupSettings()
os.environ["OPENAI_API_KEY"] = SETTINGS.openai_api_key
