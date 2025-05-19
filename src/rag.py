
import os
import tempfile
from typing import Tuple, List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# ==============================
# Clase 1: Procesamiento del PDF y creación de Vector Store
# ==============================
class PDFVectorStoreBuilder:
    def __init__(self, db_path: str = "./chroma_langchain_db", collection_name: str = "law_collection"):
        self.db_path = db_path
        self.collection_name = collection_name
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

    def process_pdf(self, uploaded_file) -> Tuple[List[Document], Chroma]:
        # Verificar si ya existe la vector store
        if os.path.exists(self.db_path) and os.listdir(self.db_path):
            vector_store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.db_path
            )
            return [], vector_store

        # Guardar temporalmente el PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        # Cargar y dividir el documento
        loader = PyPDFLoader(temp_file_path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, 
            chunk_overlap=300, 
            add_start_index=True,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        splits = text_splitter.split_documents(docs)
        print(f"🔍 Total de chunks: {len(splits)}")

        # Crear vector store
        vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.db_path
        )
        vector_store.add_documents(splits)


# ==============================
# Clase 2: Búsqueda y generación de contexto para RAG
# ==============================
class RAGRetriever:
    def __init__(self, db_path: str = "./chroma_langchain_db", collection_name: str = "law_collection"):
        self.db_path = db_path
        self.collection_name = collection_name
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.db_path
        )

    def retrieve(self, query: str, k: int = 3) -> str:
        retrieved_docs = self.vector_store.similarity_search(query, k=k)
        serialized = "\n\n".join(
            f"[Página: {doc.metadata.get('page', 'N/A')}]\n{doc.page_content}"
            for doc in retrieved_docs
        )
        return serialized