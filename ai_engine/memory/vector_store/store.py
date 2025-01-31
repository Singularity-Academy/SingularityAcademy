from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from typing import List, Dict
import pickle
import os

class VectorStore:
    def __init__(self, persist_directory: str = "vector_store"):
        self.embeddings = OpenAIEmbeddings()
        self.persist_directory = persist_directory
        self.vector_store = None
        self._initialize_store()
    
    def _initialize_store(self):
        """Initialize or load existing vector store"""
        if os.path.exists(f"{self.persist_directory}/faiss_store.pkl"):
            with open(f"{self.persist_directory}/faiss_store.pkl", "rb") as f:
                self.vector_store = pickle.load(f)
        else:
            self.vector_store = FAISS.from_texts(
                [""], embedding=self.embeddings
            )
    
    async def add_memory(self, text: str, metadata: Dict = None):
        """Add new memory to vector store"""
        try:
            self.vector_store.add_texts([text], metadatas=[metadata] if metadata else None)
            self._save_store()
        except Exception as e:
            print(f"Error adding memory: {str(e)}")
    
    async def search_memory(self, query: str, k: int = 5) -> List[str]:
        """Search for relevant memories"""
        try:
            results = self.vector_store.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
        except Exception as e:
            print(f"Error searching memory: {str(e)}")
            return []
    
    def _save_store(self):
        """Save vector store to disk"""
        os.makedirs(self.persist_directory, exist_ok=True)
        with open(f"{self.persist_directory}/faiss_store.pkl", "wb") as f:
            pickle.dump(self.vector_store, f) 