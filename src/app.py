import os
from dotenv import load_dotenv
import streamlit as st
import ollama as Ollama
from chat_utils import BaseLLM, create_llm_from_config, get_by_session_id
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from rag import PDFVectorStoreBuilder, RAGRetriever



###Environment variables
load_dotenv() 

os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")



def list_models():
    if "cached_models" in st.session_state:
        return st.session_state.cached_models
    
    models_running = Ollama.list()['models']
    # available_models = [model["model"] for model in models_running]
    available_models = [
    model["model"]
    for model in models_running
    if "nomic" not in model["model"]
    ]

    return available_models


st.set_page_config(page_title="Asistente de Leyes colombianas", layout="centered")
# st.image("public/logo_dark.png", use_container_width=True) 
# st.title('Ollama Chatbot')
st.write('Estoy para ayudarte a comprender la ley colombiana')

# # Initialization
# Get models once
if "cached_models" not in st.session_state:
    st.session_state.cached_models = list_models()

if "session_id" not in st.session_state:
    st.session_state.session_id = "default"

if 'historial' not in st.session_state:
    st.session_state.historial = []

# Sidebar con controles
with st.sidebar:
    st.write('## Model Selection')
    st.session_state.model_selection = st.selectbox(
        'Select a model',
        options=st.session_state.cached_models,
        index=0
    )

    uploaded_pdf = st.file_uploader("Añade pdf de la reforma pensional", accept_multiple_files=False)
    
    st.session_state.temperature = st.slider(
        'Temperatura',
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )
    
    st.session_state.top_p = st.slider(
        'Top P',
        min_value=0.0,
        max_value=1.0,
        value=0.9,
        step=0.1
    )
    
    st.session_state.top_k = st.slider(
        'Top K',
        min_value=0,
        max_value=100,
        value=40,
        step=1
    )
    
    st.session_state.max_tokens = st.slider(
        'Max Tokens',
        min_value=1,
        max_value=4096,
        value=256,
        step=1
    )

    # Campo de entrada de usuario
user_input = st.chat_input('Haz tu pregunta:')

if user_input and uploaded_pdf:
    with st.chat_message("user"):
        # st.write(user_input)
        st.markdown(user_input)
        print(f"Input del usuario: {user_input}")  # Debug 1

    try:
        with st.chat_message("assistant"):
            with st.spinner("🧠 El modelo está pensando..."):
                response_area = st.empty()
                
                # --- Get base model configuration ---
                llm_config = BaseLLM(
                    input_text=user_input,
                    model=st.session_state.model_selection,
                    temperature=st.session_state.temperature,
                    top_p=st.session_state.top_p,
                    top_k=st.session_state.top_k,
                    max_tokens=st.session_state.max_tokens
                )

                # --- Get Model and prompt template ---
                llm, prompt_template = create_llm_from_config(llm_config)

                chain = prompt_template | llm

                # --- Get Model and prompt template ---
                chain_with_history = RunnableWithMessageHistory(
                    chain,
                    # Uses the get_by_session_id function defined in the example
                    # above.
                    get_by_session_id,
                    input_messages_key="input",
                    history_messages_key="history",
                )

                # 📝 Process attached PDF
                builder = PDFVectorStoreBuilder()
                docs, vector_store = builder.process_pdf(uploaded_pdf)

                # 📝 Use RAG
                retriever = RAGRetriever()
                contexto = retriever.retrieve(user_input)

                # --- Prompt formatter and historical ---
                prompt = prompt_template.format(context=contexto, input=user_input)

                respuesta = chain_with_history.invoke(
                    {
                        "input": user_input,
                        "context": contexto
                    },
                    config={"configurable": {"session_id": st.session_state.session_id}}
                )

                response_area.markdown(respuesta.content)

                # Mostrar historial de mensajes actual
                history = get_by_session_id(st.session_state.session_id)
                with st.expander("🗂️ Historial de conversación"):
                    for msg in history.messages:
                        st.write(f"**[{msg.type}]**: {msg.content}")


    except Exception as e:
        print(f"ERROR: {str(e)}")  # Debug 10 (importante)
        st.error(f"Error en la comunicación: {str(e)}")
