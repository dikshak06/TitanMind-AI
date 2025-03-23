import streamlit as st
from langchain_ollama import ChatOllama  

from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import(
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)
# Streamlit Page Config
st.set_page_config(page_title="TitanMind AI", page_icon="🤖")

# Title
st.title("🤖 TitanMind AI ")
st.caption("🚀 Your AI Programmer with Debugging Superpowers 🚀")
with st.sidebar:
    st.header("⚙️ Model Configuration")
    selected_model=st.selectbox(
        "Choose Model",
        ["deepseek-r1:1.5b","deepseek-r1:7b","Add Model Name"],
        index=0
    )
    st.divider()
    st.markdown("### Model Capabilities")
    st.markdown("""
       - 🐍💻 Python Expert 
       - 🛠️🔍 Debugging Assistant 
       - 📄✍️ Code Documentation 
       - 🎨🧩 Solution Design 
                
    """)
    st.divider()
    st.markdown("Built with [Ollama](https://ollama.ai/) | [LangChain](https://python.langchain.com/)")
    st.header("Developed by :: ")
    st.markdown("""
       - 💻👨‍💻 Devesh Agale 💻👨‍💻 
       - 💻👨‍💻 Diksha Kulkarni 💻👨‍💻 
                
    """)

#####################################################################################################
def generate_ai_response(prompt_chain):
    processing_pipeline=prompt_chain | llm_engine | StrOutputParser()
    return processing_pipeline.invoke({})


def build_prompt_chain():
    prompt_sequence=[system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

#####################################################################################################

    #initiate the Chat engine
llm_engine=ChatOllama(model=selected_model,
                      base_url="http://localhost:11434",
                      tempereture=0.3)
system_prompt=SystemMessagePromptTemplate.from_template(
    "Always respond in English. You are an Expert AI coding asistant. Provide concise, correct solutions "
    "with strategic print statements for debugging. ")
#Session State Management
if "message_log" not in st.session_state:
    st.session_state.message_log=[{"role": "ai", "content": "Hi! I'm TitanMind AI 🤖. How can I help you code today? 💻"}]

#Chat Container
chat_container=st.container()

#Display Chat Message
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

user_query=st.chat_input("Type your Coding Question here...")
if user_query:
    st.session_state.message_log.append({"role": "user", "content": user_query})

    #Generate AI response
    with st.spinner("💭🤔Processing...thinking please wait.......💭"):
        prompt_chain= build_prompt_chain()
        ai_response= generate_ai_response(prompt_chain)

    #add AI response to log
    st.session_state.message_log.append({"role":"ai","content":ai_response})

    #Rerun to update chat display
    st.rerun()