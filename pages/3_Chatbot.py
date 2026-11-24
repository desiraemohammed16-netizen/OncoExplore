# Lab 3: Chatbot page
# TODO: Rename this file to fit your page. Keep the number at the front.
#
# A chatbot built with Pydantic AI (see the Pydantic AI pages on Canvas).
# It should:
#   - use a Pydantic AI Agent with instructions that fit your project's theme (no tools yet)
#   - use Streamlit's chat elements: st.chat_message and st.chat_input
#   - remember the conversation (message_history, saved in st.session_state)
#   - use try/except so an error shows a message instead of crashing the page
#   - stay on theme, without using any API or external data
#
# Your Gemini API key goes in .streamlit/secrets.toml as GOOGLE_API_KEY.

import streamlit as st
from pydantic_ai import Agent
import os

# AI-assisted fix: load Streamlit's private key before creating the agent.
try:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"].strip()
except (FileNotFoundError, KeyError):
    st.error("Add GOOGLE_API_KEY to .streamlit/secrets.toml and restart Streamlit.")
    st.stop()

agent = Agent(
    "google:gemini-3.5-flash-lite",
    instructions=(
        "You are a friendly assistant for information about lung, breast, prostate, and leukemia cancers. "
        "Talk about survival rates, available treatments, status of clinical trials, and breakdown population of diagnosed patients."
        "Do not provide any medical advice, but you may share risk factors."
        "Be able to explain how treatments and clinical trials work"
        "Explain what each cancer is and its stages if asked and how it is diagnosed. "
        "Limit answers to three normal length sentences."
        "If you cannot answer a question, say 'I can't answer that, what else would you like to know?' and do not answer."
        "Respond sensitively when asked questions pertaining to cancer only discolose survival rate if asked."
    ),
)
st.title("Cancer Info Chatbot")
st.write("Chat with this AI assistant to learn about lung, breast, prostate, and leukemia cancers.")
#remeber: session_state is a dictionary - think about keys
#will need keys for memory, user type, and proabbaly inputs...
#thinking save new message after displaying old ones
if "memory" not in st.session_state:
    st.session_state["memory"] = [] #checks for key
#repeat for message_history
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []
with st.chat_message("assistant"):
    st.write("Hello! What would you like to know about?")
for message in st.session_state["message_history"]:#loop to show messages
    with st.chat_message(message["userType"]):
        st.write(message["inputInfo"])
prompt=st.chat_input("Type questions here:")#making input box 
if prompt:#==True: #user inputted something
    with st.chat_message("user"):#show the inputted thing
        st.write(prompt)    
    st.session_state["message_history"].append({"userType":"user","inputInfo":prompt})#save as messages; not AI conversation in memory
    with st.chat_message("assistant"):
        try:
            result = agent.run_sync(prompt, message_history=st.session_state["memory"])
            st.write(result.output)#see Ai's message response
            st.session_state["memory"] = result.all_messages()#whole conversation so far is saved/remembered
            st.session_state["message_history"].append({"userType":"assistant","inputInfo":result.output})#save messages

        except:
            st.write(f"An error occurred! Yikes!!")
