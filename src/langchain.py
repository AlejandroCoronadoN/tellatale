import asyncio

from langchain.agents import AgentExecutor, OpenAIFunctionsAgent, Tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.schema import AIMessage, HumanMessage
from tools.users import process_user_flow, retrieve_user
from tools.journal import create_journal_entry
from tools.profiling import question_profile, create_recommendation

from framework.common import llm, streaming_callback

MEM_KEY = "chat_history"

memory = ConversationBufferMemory(
    memory_key=MEM_KEY,
    return_messages=True,
    input_key="input",
    output_key="output",
)
bot_tools = [
    Tool(
        name="retrieve_user",
        func=retrieve_user,
        description="""When a user interacts for the first time, answer with a funny, wholesome reply and ask if they have met before. Then proceed to ask her name. You will infer the user name and pas it to this function. The function expects a string with a user_name delimited by a string for example 'Alejandro Coronado'.  If the user doesn't provide his name ask for it.
        """,
        coroutine=retrieve_user,
        return_direct=True,
    ),
    Tool(
        name="process_user_flow",
        func=process_user_flow,
        description="""This tool expects a json entry with the user information stored in the internal storage. You will identify the following parameters:
        {'name': 'Alejandro Coronado' , 'user_id': '10001', 'profiled': 'True' , 'journal': 'True' 'recommended':'True' }.
        Depending on the entries  you will perform the following tasks in order of priority.

        1. If 'profiled' is 'False' execute question_profile Tool passing 'user_id' value as an input like this '10001',
        Just after this Execute create_journal_entry Tool passing 'user_id' value as an input like this '100001'

        2. If 'journal' is 'False' Execute create_journal_entry Tool passing 'user_id' value as an input like this '100001'

        """,
        # TODO:  3. if 'recommended' is 'False' execute create_recommendationTool passing 'user_id' value as an input like this '100001'
        coroutine=process_user_flow,
        return_direct=True,
    ),
    Tool(
        name="create_journal_entry",
        func=create_journal_entry,
        description=""""Use this Tool when 'Execute create_journal_entry' is passed by the user.  Also, it can be used when the user  pass an entry of a personal journal. This journal contains information about the user experience in a particular date. The input for this function will be represented by the following format 'user_id|journal_entry' for example:

        For example a user might tell you how his day was going. The function expects a string with a user_id and a journal_entry delimited by a pipe.

        For example '100001| Today was a very sad day but I play vim-adventures and everything start going well'

        The user id_can be inferred by the context or it will be passed by other Tools calling this tool.
        """,
        coroutine=create_journal_entry,
        return_direct=True,
    ),
    Tool(
        name="question_profile",
        func=question_profile,
        description="""Use this Tool when 'Execute question_profile|user_id|stage|answer' is passed by the user.  Or when the user answers any of the following questions

        1. What's your favorite thing to do?
        2. Which of the following movies you like the most? Lord of the rings, Harry Potter, Mulan.
        3. Tell me about your day?

        The question_profile function only expects two arguments 'user_id|stage|answer'. This user id_will be provided by the request and it will be passed. This is an example of the user input '100001|1|play the piano'

        The response from this Tool can only be one of:
        1. What's your favorite thing to do?
        2. Which of the following movies you like the most? Lord of the rings, Harry Potter, Mulan.
        3. Tell me about your day?
        """,
        coroutine=question_profile,
        return_direct=True,
    ),
    Tool(
        name="create_recommendation",
        func=create_recommendation,
        description="Use this Tool when 'Execute create_recommendation' is passed by the user. This Tool creates a recommendation of the best psychologist for the user. For the moment just reply with 'The best psychologist for you is Biaani Garfias, contact her at 951-100-00-00' ",
        coroutine=create_recommendation,
        return_direct=True,
    ),
]
system_msg = SystemMessage(
    content="""
    You work for Amaru Psicologia. Amaru is a company that provides psychological help by connecting users with the best psychologist.\n
    You are a very skilled Human Resources agent that understands the different types of psychological therapy.
    You are proficient in psychoanalyst and psychology. \n
    You can never respond to inapproriate or out of scope questions.\n

    You always use a 'tool' in order to find answers to questions.\n
    If a tool does not satisfy the query then simply say you don't know the answer and reply by suggesting creating a psychological advisory session with one of our experts at  https://amaru.mx/asesoria \n
    Your tools allow you to answer questions about product documentation, branch information, and product stock.\n Nothing else.
    Don't make up information that is not directly quotable from sources. If you do not know the answer then apologize and ask the user if they want to talk to a customer respresentative.\n
    Some sample questions and their tools are:\n
    User is not register, or first interaction with promt -> user_login
    Today was a very difficult day at work, after I wake up I had a coffee and then my boss called me. My day was ruined-> create_journal_entry
    what is the the best game to play in ps5> out of scope, do not answer
    Give me a psychologist recommendation -> question_profile
    """
)
prompt = OpenAIFunctionsAgent.create_prompt(
    system_message=system_msg,
    extra_prompt_messages=[MessagesPlaceholder(variable_name=MEM_KEY)],
)

agent = OpenAIFunctionsAgent(llm=llm, prompt=prompt, tools=bot_tools)

agent_executor = AgentExecutor(
    agent=agent,
    tools=bot_tools,
    verbose=True,
    memory=memory,
    return_intermediate_steps=True,
)


async def create_stream_response(
    message: str, chat_history: list
) -> asyncio.StreamReader:
    """Creates a stream of responses from the AI agent for the given prompt.

    Args:
        message (str): messaged prompt for AI agent
    Returns:
        asyncio.StreamReader: Stream of responses from the AI agent
    """
    task = asyncio.create_task(agent_executor.acall({"input": message}))
    total_tokens = 0
    while True:
        if task.done():
            break
        try:
            # get the token from async queue
            token = await asyncio.wait_for(streaming_callback.queue.get(), timeout=1)
            if token:
                total_tokens += len(token.strip())
                yield token

        except asyncio.TimeoutError:
            pass

    if total_tokens == 0 and "output" in task.result().keys():
        yield task.result()["output"]
    while not streaming_callback.queue.empty():
        yield await streaming_callback.queue.get()
    if streaming_callback.queue.empty():
        await streaming_callback.clear_queue()
    await task


async def main():
    # Example data
    chat_history = []
    cont = 0
    new_message = ""
    while True:
        if new_message == "":
            message = input("You: ")  # Take user input
        else:
            message = new_message
            new_message = ""
        if message.lower() == "exit":
            break  # Exit the loop if the user types 'exit'
        # Add the user input to the chat history
        async for response in create_stream_response(message, chat_history):
            if "Execute question_profile" in response:
                user_id = response.split("|")[1].split(":")[1]
                new_message = f"Execute question_profile|{user_id}|0|na"
            # Assuming the response is a string, you can add it to the chat history
            chat_history.append({"role": "user", "content": message})
            chat_history.append(HumanMessage(content=message))
            chat_history.append(AIMessage(content=response))
            # Raise an exception or break the loop if needed
            # raise ValueError
        cont += 1
        print(cont)


if __name__ == "__main__":
    # Get the event loop and run the main coroutine
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
