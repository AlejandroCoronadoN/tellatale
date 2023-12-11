"""Find info about branches."""
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from config.configuration import SETTINGS
from langchain.chat_models import ChatOpenAI
from langchain.retrievers import MultiQueryRetriever
import os


def continue_flow(user_info: str):
    """Parses user information from a string."""
    # Your parsing logic here
    values = user_info.split("|")
    profiled = values[2].split(":")[1]
    journal = values[3].split(":")[1]

    if "False" in profiled:
        return f"Execute question_profile|{user_info}"
    if "False" in journal:
        return f"Execute create_journal_entry|{user_info}"
    return values


# Assuming this script is in the root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "users.csv")


loader = CSVLoader(file_path=file_path)
data = loader.load()
contacts = FAISS.from_documents(data, embedding=OpenAIEmbeddings())


def parse_document(doc):
    # Parse the content
    content_lines = doc.page_content.split("\n")
    user_info = ""

    for line in content_lines:
        # Split each line into key and value using ':'
        parts = line.split(":")

        # Remove leading/trailing whitespaces from key and value
        key = parts[0].strip()
        value = parts[1].strip()

        # Store key-value pair in a dictionary
        user_info += f"{key}:{value}|"
    return user_info


async def retrieve_user(user_name: str):
    """When a user pass his name retrieve relevant documents based on the input query. The input passed to this function represents the name of the user 'Alejandro Coronado'. This user_name will be used to create a query over the contacts database using CSVLoader.

    Args:
        input (str): The input query.

    Returns:
        list: A list of relevant documents.
    """
    llm = ChatOpenAI(temperature=0, model_name=SETTINGS.agent_model_name)
    retriever_from_llm = MultiQueryRetriever.from_llm(
        retriever=contacts.as_retriever(), llm=llm
    )
    input = f"Search for the following user in the csv files and return the information related to this user as a json:  {user_name}"
    result = retriever_from_llm.get_relevant_documents(input)
    user_info = parse_document(result[0])
    user_info = continue_flow(user_info)
    return user_info


async def log_user(user_name: str) -> str:
    """Searches for the user inside a users.csv and returns the user associated information as json file

    Args:
        user_name (str): User's Zip code

    Returns:
        str:  Formatted message with all the near branches information.
    """
    if user_name:
        return f"Hello! {user_name}"
    else:
        return "I'm sorry, it seems that the Name you provided is not a valid argument, can you repeat your name?"


async def process_user_flow(user_info: str) -> str:
    """Dictates the next stage for the chatbot after registering a client
    Args:
        user_name (str): User's Zip code

    Returns:
        str:  Formatted message with all the near branches information.
    """
    if user_info:
        if not user_info["profiled"]:
            return ["Execute question_profile"]
        elif user_info["journal"]:
            return ["Execute create_journal_entry"]
    else:
        return "I'm sorry, I can't process you data, we are having problems with out application. Return in a couple of minutes :D"
