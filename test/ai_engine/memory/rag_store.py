from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List, Dict
import json

class RAGStore:
    def __init__(self, persist_directory: str):
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
    async def add_interaction(self, interaction: Dict):
        # Convert interaction to document format
        doc = Document(
            page_content=json.dumps(interaction["content"]),
            metadata={
                "type": interaction["type"],
                "timestamp": interaction["timestamp"],
                "session_id": interaction.get("session_id")
            }
        )
        
        # Split and store
        texts = self.text_splitter.split_documents([doc])
        self.vector_store.add_documents(texts)
        
    async def search_similar(self, query: str, k: int = 5) -> List[Document]:
        return self.vector_store.similarity_search(query, k=k) 