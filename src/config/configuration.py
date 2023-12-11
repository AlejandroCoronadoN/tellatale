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

    app_name: str = "Reece Chat"
    log_level: str = "info"
    openai_api_key: str
    max_message_history: int = 5
    temperature: float = 0.4
    agent_model_name: str = "gpt-3.5-turbo"
    version: str = "0.1.0"
    minimum_delay_ms: int = 5
    maximum_delay_ms: int = 10


SETTINGS = StartupSettings()
os.environ["OPENAI_API_KEY"] = SETTINGS.openai_api_key
