"""Frontend."""
import os

import requests
import yaml
from config.configuration import SETTINGS
from loguru import logger
from yaml.loader import SafeLoader

# load the vector store
bot_image = "assets/bot.png"
human_image = "assets/human.png"


logger.add("logs.log", rotation="10 MB", level="INFO")

os.environ["OPENAI_API_KEY"] = SETTINGS.openai_api_key

if "config" not in st.session_state:
    with open("src/config/credentials.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)


authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)
name, authentication_status, st.session_state.uname = authenticator.login(
    "Login", "main"
)


if authentication_status:
    st.markdown(
        '<h1 style="color: #093463;"><img src="https://i.imgur.com/YkQHYH4.png" width=50> Reece Chat Demo</h1>',
        unsafe_allow_html=True,
    )
    conv_id = requests.post(
        "http://localhost:8000/agents/create_conversation", json={}
    ).json()["id"]
    logger.info(conv_id)
    st.session_state.conv_id = conv_id

    authenticator.logout("Logout", "main", key="unique_key")
    st.write(f"Welcome *{name}*")

elif authentication_status is False:
    st.error("st.session_state.uname/password is incorrect")

elif authentication_status is None:
    st.warning("Please enter your st.session_state.uname and password")
if st.session_state["authentication_status"]:
    restart = st.button("Restart Chat")
    if "messages" not in st.session_state or restart:
        if restart:
            st.success("Session Restarted 🏁")
        st.session_state.messages = []
        conv_id = requests.post(
            "http://localhost:8000/agents/create_conversation", json={}
        ).json()["id"]
        logger.info(conv_id)
        st.session_state.conv_id = conv_id

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message(message["role"], avatar=human_image):
                st.markdown(message["content"].content)

    # Accept user input
    if prompt := st.chat_input("How can I help?"):
        logger.info(f"{name}: {prompt}")
        # Add user message to chat history
        # Display user message in chat message container
        with st.chat_message("user", avatar=human_image):
            st.markdown(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant", avatar=bot_image):
            with st.spinner("Thinking..."):
                runner = st.image(
                    "https://media.giphy.com/media/dw2jpsey5a5I4/giphy.gif"
                )
                try:
                    message = requests.post(
                        "http://localhost:8000/agents/chat-agent",
                        json={
                            "conversation_id": st.session_state.conv_id,
                            "message": prompt,
                        },
                    ).json()["response"]
                except Exception:
                    message = "Hey, it's the frontend here... I had issues talking with the backend... We're working through our communication issues. Sorry for the inconvenience."
                runner.empty()
                logger.info(f"Assistant: {message}")

            st.session_state.messages.append({"role": "assistant", "content": message})
            message_placeholder = st.write(message)

            if "balloons" in prompt:
                st.balloons()


elif st.session_state["authentication_status"] is False:
    st.error("st.session_state.uname/password is incorrect")

elif st.session_state["authentication_status"] is None:
    st.warning("Please enter your st.session_state.uname and password")
