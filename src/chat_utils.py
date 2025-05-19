from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.chat_history import BaseChatMessageHistory
from typing import List, Dict


#####Base LLM class to create model
class BaseLLM(BaseModel):
    input_text: str
    model: str
    temperature: float
    top_p: float
    top_k: int
    max_tokens: int


# Configuración de LangChain
SYSTEM_PROMPT = "OLAK" #system_prompt_get( )


def create_llm_from_config(config: BaseLLM):
    llm = ChatOllama(
        model=config.model,
        temperature=config.temperature,
        num_predict=config.max_tokens,
        system=SYSTEM_PROMPT,
        disable_streaming=False,
        top_k=config.top_k,
        top_p=config.top_p

        # metadata={}
        # stream=True
    )
    
    prompt_template = ChatPromptTemplate([
        # ("system", SYSTEM_PROMPT),
        ("human", 
         """Utiliza la siguiente información de referencia para responder:
         [Contexto relevante]
         {context}

         [Pregunta del usuario]
         {input}

         """)
            # [Instrucciones]
            # - Responde como un experto de 25 años en motores.
            # - Sé técnico, claro y detallado.
            # - No repitas la pregunta ni menciones que estás usando contexto.
            # - Si no sabes algo, dilo con honestidad.

    ])
    return llm, prompt_template


#####Class for memory object
class InMemoryHistory(BaseChatMessageHistory):
    """Historial de mensajes en memoria."""
    messages: List[BaseMessage] = []

    def __init__(self):
        self.messages = []

    def add_messages(self, messages: List[BaseMessage]) -> None:
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []

# Almacén global (fuera del modelo)
_memory_store: Dict[str, InMemoryHistory] = {}

def get_by_session_id(session_id: str) -> InMemoryHistory:
    if session_id not in _memory_store:
        _memory_store[session_id] = InMemoryHistory()
    return _memory_store[session_id]
