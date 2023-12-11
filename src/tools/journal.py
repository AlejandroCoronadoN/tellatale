"""Find info about branches."""
from tools.users import retrieve_user
import pandas as pd
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.agents import tool
from langchain.chat_models import ChatOpenAI
from config.configuration import SETTINGS
from langchain.retrievers import MultiQueryRetriever
import os

# Assuming this script is in the root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
journal_path = os.path.join(current_dir, "journals.csv")

loader = CSVLoader(file_path=journal_path)
data = loader.load()
journals = FAISS.from_documents(data, embedding=OpenAIEmbeddings())
JOURNAL_DATA = pd.read_csv(journal_path)


@tool
async def retrieve_journal(user_name: str):
    """Retrieves relevant documents based on the input query.

    Args:
        input (str): The input query.

    Returns:
        list: A list of relevant documents.
    """
    llm = ChatOpenAI(temperature=0, model_name=SETTINGS.agent_model_name)
    retriever_from_llm = MultiQueryRetriever.from_llm(
        retriever=journals.as_retriever(), llm=llm
    )
    input = f"Search for the following user in the csv files and return the information related to this user as a json:  {user_name}"
    result = retriever_from_llm.get_relevant_documents(input)
    return result


async def create_journal_entry(user_id: str, journal_entry: str) -> str:
    """This function stores a user journal entry. It expects a

    For example '100001| Today was a very sad day but I play vim-adventures and everything start going well'

    Args:
        user_id (str): User's Zip code

    Returns:
        str:  Formatted message with all the near branches information.
    """
    if user_id in JOURNAL_DATA.user_id.uniqiue():
        print("The user was previously logged")
    else:
        new_entry = {
            "user_id": "10001",
            "date": "1 January 2024",
            "journal_entry": "Today is going to be a great day",
        }
        # JOURNAL_DATA
        print(new_entry)
        # TODO append to JOURNAL_DATA AND SAVE


async def create_magic_journal(user_id: str) -> str:
    """Reads all the entries inside journals.csv and filters the entries associated with the user_id.  Then for each entry creates a customized story. using additional information stored in the users.csv storage.
    Args:
        user_id (str): User's Id

    Returns:
        str:  Formatted message with all the near branches information.
    """
    if user_id:
        journal = retrieve_journal(user_id)
        users = retrieve_user(user_id)
        print(journal)
        print(users)
        return "CREATE_MAGIC_JOURNAL"
    else:
        return "I'm sorry, I can't tell you a magic story this time. Please try again in a couple of minutes."
