"""
RAG System Configuration for Raga Remix Studio
Centralized configuration for embeddings, vector store, and LLM
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class RAGConfig:
    """Centralized RAG configuration"""
    
    # ===== API KEYS =====
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # ===== EMBEDDING CONFIGURATION =====
    EMBEDDING_MODEL = "text-embedding-3-small"
    EMBEDDING_DIMENSIONS = 1536
    EMBEDDING_BATCH_SIZE = 100
    
    # ===== CHUNKING CONFIGURATION =====
    CHUNK_SIZE = 512
    CHUNK_OVERLAP = 50
    SEPARATORS = ["\n\n", "\n", ". ", " ", ""]
    
    # ===== RETRIEVAL CONFIGURATION =====
    TOP_K = 5
    SCORE_THRESHOLD = 0.5
    SEARCH_TYPE = "similarity"
    
    # ===== LLM CONFIGURATION =====
    LLM_MODEL = "gpt-4o-mini"
    LLM_TEMPERATURE = 0.1
    LLM_MAX_TOKENS = 1000
    LLM_TOP_P = 0.95
    
    # ===== VECTOR STORE =====
    VECTOR_STORE_TYPE = "chroma"
    CHROMA_PERSIST_DIR = "./chroma_db"
    
    # ===== CONTEXT MANAGEMENT =====
    MAX_CONTEXT_TOKENS = 3000
    INCLUDE_METADATA = True
    
    # ===== DIRECTORIES =====
    PROJECT_ROOT = Path(__file__).parent
    KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "knowledge_base"
    LOGS_DIR = PROJECT_ROOT / "logs"
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in environment")
        return True

# Validate on import
RAGConfig.validate()
