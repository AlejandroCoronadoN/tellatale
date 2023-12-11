"""Profile users using questions."""
import pandas as pd
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.agents import tool
from config.configuration import SETTINGS
from langchain.chat_models import ChatOpenAI
from langchain.retrievers import MultiQueryRetriever
import os

# Assuming this script is in the root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "psychologists.csv")
users_path = os.path.join(current_dir, "users.csv")

users = pd.read_csv(users_path)
loader = CSVLoader(file_path=file_path)
data = loader.load()
psychologists = FAISS.from_documents(data, embedding=OpenAIEmbeddings())


def save_answer(user_id, answer, stage):
    users.loc[(users.user_id == user_id), "question_{stage}"] = answer
    users.to_csv(users_path)


@tool
async def retrieve_psychologist_information(psychologist_name: str):
    """Asks the following question and returns the answer as a single string
    "How's been you day, are you sleeping well?

    Args:
        input (str): The input query.

    Returns:
        list: A list of relevant documents.
    """
    llm = ChatOpenAI(temperature=0, model_name=SETTINGS.agent_model_name)
    retriever_from_llm = MultiQueryRetriever.from_llm(
        retriever=psychologists.as_retriever(), llm=llm
    )
    input = f"Search for the following psychologist in the csv files and return the information related to this user as a json:  {psychologist_name}"
    result = retriever_from_llm.get_relevant_documents(input)
    return result


async def create_recommendation(user_id: str) -> str:
    """Searches inside the psychologist database and returns the best psychologist for the user.

    Args:
        user_id (str): User's Id

    Returns:
        str:  Formatted message with all the near branches information.
    """
    if user_id:
        text_reply = retrieve_psychologist_information(user_id=user_id)
        return text_reply
    else:
        return "I'm sorry, it seems like the ZIP code entered is incorrect. Please provide a valid ZIP code."


async def question_profile(user_stage: str) -> str:
    """This Tool makes three questions to the user. This function is only executed once for each user session and the data is stored in the system.

    Args:
        user_id (str): User's Id

    Returns:
        str:  Formatted message with all the near branches information.
    """
    user_id = user_stage.split("|")[0]
    stage = user_stage.split("|")[1]
    answer = user_stage.split("|")[2]
    if answer != "na":
        save_answer(user_id, answer, stage)
    if user_stage:
        if stage == "0":
            return "1.What's your favorite thing to do?"
        elif stage == "1":
            return "2. Which of the following movies you like the most? Lord of the rings, Harry Potter, Mulan."
        elif stage == 2:
            return "3. Tell me about your day? "

    else:
        return f"I'm sorry, I can't make a profile with the information you passed:\n {user_stage}."
