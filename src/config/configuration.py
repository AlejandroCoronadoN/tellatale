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
    agent_model_name: str = "gpt-4"
    version: str = "0.1.0"
    sop_disclaimer: str = """\n \n *** \n **Reminder**: The response provided is believed to be accurate, however, 100% accuracy isn’t guaranteed. It’s always a good idea to check the SOPs (if available) or contact your supervisor for confirmation."""
    hr_disclaimer: str = """\n \n *** \n **Reminder**: The response provided is believed to be accurate, however, 100% accuracy isn’t guaranteed. It’s always a good idea to check the provided documents (if available) or contact People Experience at [HR@reece.com.](mailto:hr@reece.com)"""

    headers: dict[str, str] = {"X-Max-Api-Secret": "1upRhSWC1B"}
    reece_api_url: str = "https://api.reece.com"
    reece_base_url: str = "https://www.reece.com"
    system_message: str = """
    You work for Reece USA.
    You can answer HR related questions and help employees find certain products, and answer SOP related questions.
    Your name is ReeceBot 4000.
    For HR related questions, only use the provided documents to answer question, don't include other sources or fabricate information. Provide a page number and link to the source documents if applicable.
    If you do not know the answer to a question, don't make stuff up, just state you do not know.
    Keep answers short and sweet.
"""

    qdrant_host: str = "10.248.35.157"
    qdrant_port: int = 80
    qdrant_grpc_port: int = 80
    # Microsoft Bot Framework Sesttings
    app_id: str = os.environ.get(
        "MicrosoftAppId", "709c31a7-d9f5-46d0-98a9-9abd200ff5aa"
    )
    app_password: str = os.environ.get(
        "MicrosoftAppPassword", "qaS8Q~EpA118Ef1ceiZhH9ju.dnG0A25TzrCFdk7"
    )

    fortiline_credentials: str = "default"
    fortiline_url: str = "http://54.146.183.14/"
    fortiline_index: str = "Fortiline_VA"

    error_message: str = (
        "I encountered an error. Please try your request at a later time."
    )
    minimum_delay_ms: int = 5
    maximum_delay_ms: int = 10


SETTINGS = StartupSettings()
os.environ["OPENAI_API_KEY"] = SETTINGS.openai_api_key
