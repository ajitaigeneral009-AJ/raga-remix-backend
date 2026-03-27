"""
RAG Service for Raga Remix Studio
Handles intelligent query answering using RAG pipeline
"""

import logging
from typing import Dict, List
from datetime import datetime

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate

from rag_config import RAGConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RagaMusicRAG:
    """RAG system for intelligent music knowledge retrieval"""

    def __init__(self):
        logger.info("🎵 Initializing RAG system...")

        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=RAGConfig.EMBEDDING_MODEL,
            openai_api_key=RAGConfig.OPENAI_API_KEY,
        )

        # Load vector store
        self.vectorstore = Chroma(
            persist_directory=RAGConfig.CHROMA_PERSIST_DIR,
            embedding_function=self.embeddings,
        )

        # Initialize LLM
        self.llm = ChatOpenAI(
            model=RAGConfig.LLM_MODEL,
            temperature=RAGConfig.LLM_TEMPERATURE,
            max_tokens=RAGConfig.LLM_MAX_TOKENS,
            openai_api_key=RAGConfig.OPENAI_API_KEY,
        )

        # Create retriever
        self.retriever = self.vectorstore.as_retriever(
            search_type=RAGConfig.SEARCH_TYPE,
            search_kwargs={"k": RAGConfig.TOP_K},
        )

        # Define prompt template
        self.prompt_template = PromptTemplate(
            template=(
                "You are an expert in Indian classical music, ragas, instruments, "
                "and fusion music styles.\n"
                "Use the following context to answer the question accurately and concisely.\n\n"
                "Context:\n{context}\n\n"
                "Question: {question}\n\n"
                "Answer (provide factual information based on the context):"
            ),
            input_variables=["context", "question"],
        )

        logger.info("✅ RAG system initialized successfully")

    # ------------------------------------------------------------------ #
    # Main query method
    # ------------------------------------------------------------------ #

    def query(self, question: str, include_sources: bool = True) -> Dict:
        """
        Query the RAG system with a music-related question.

        Args:
            question: User's question.
            include_sources: Whether to include source documents.

        Returns:
            Dictionary with answer and metadata.
        """
        start_time = datetime.now()

        try:
            logger.info(f"🔍 Processing query: {question}")

            # 1) Retrieve relevant documents
            docs = self.retriever.invoke(question)

            # 2) Build context string
            context = "\n\n".join(doc.page_content for doc in docs)

            # 3) Format prompt
            prompt = self.prompt_template.format(context=context, question=question)

            # 4) Call LLM
            response = self.llm.invoke(prompt)
            answer_text = getattr(response, "content", str(response))

            processing_time = (datetime.now() - start_time).total_seconds() * 1000

            # Build response
            result: Dict = {
                "answer": answer_text,
                "metadata": {
                    "retrieved_docs": len(docs),
                    "processing_time_ms": round(processing_time, 2),
                },
                "confidence": 0.0 if not docs else min(1.0, len(docs) / 5.0),
            }

            if include_sources and docs:
                result["sources"] = [
                    {
                        "content": doc.page_content[:500],  # truncate for brevity
                        "metadata": doc.metadata,
                    }
                    for doc in docs
                ]

            logger.info(f"✅ Query processed in {processing_time:.2f} ms")
            return result

        except Exception as e:
            logger.error(f"❌ Error processing query: {e}")
            raise

    # ------------------------------------------------------------------ #
    # Helper search methods
    # ------------------------------------------------------------------ #

    def search_instruments_by_category(self, category: str, limit: int = 5) -> Dict:
        """Search instruments by category."""
        try:
            query = (
                f"List {limit} instruments in the {category} category "
                f"with their properties"
            )

            docs = self.vectorstore.similarity_search(
                query,
                k=limit,
                filter={"type": "instrument"},
            )

            instruments: List[Dict] = []
            for doc in docs:
                instruments.append(
                    {
                        "name": doc.metadata.get("name"),
                        "category": doc.metadata.get("category"),
                        "content": doc.page_content[:300],
                    }
                )

            return {
                "category": category,
                "count": len(instruments),
                "instruments": instruments,
            }

        except Exception as e:
            logger.error(f"❌ Error searching instruments: {e}")
            raise

    def search_ragas_by_mood(self, mood: str, limit: int = 3) -> Dict:
        """Search ragas that match a specific mood."""
        try:
            query = f"Find ragas suitable for {mood} mood with their characteristics"

            docs = self.vectorstore.similarity_search(
                query,
                k=limit,
                filter={"type": "raga"},
            )

            ragas: List[Dict] = []
            for doc in docs:
                ragas.append(
                    {
                        "name": doc.metadata.get("name"),
                        "mood": doc.metadata.get("mood"),
                        "time": doc.metadata.get("time"),
                        "content": doc.page_content[:400],
                    }
                )

            return {
                "mood": mood,
                "count": len(ragas),
                "ragas": ragas,
            }

        except Exception as e:
            logger.error(f"❌ Error searching ragas: {e}")
            raise

    def recommend_fusion_style(self, preferences: str) -> Dict:
        """Recommend fusion style based on user preferences."""
        try:
            query = f"Recommend a fusion style for: {preferences}"

            docs = self.vectorstore.similarity_search(
                query,
                k=3,
                filter={"type": "fusion_style"},
            )

            # Use LLM to generate recommendation
            context = "\n\n".join(doc.page_content for doc in docs)

            prompt = (
                "Based on these fusion styles:\n\n"
                f"{context}\n\n"
                f"Recommend the best fusion style for: {preferences}\n\n"
                "Provide a brief recommendation with reasoning."
            )

            response = self.llm.invoke(prompt)

            return {
                "preferences": preferences,
                "recommendation": getattr(response, "content", str(response)),
                "considered_styles": [doc.metadata.get("name") for doc in docs],
            }

        except Exception as e:
            logger.error(f"❌ Error generating recommendation: {e}")
            raise


# Global singleton instance
_rag_system: RagaMusicRAG | None = None


def get_rag_service() -> RagaMusicRAG:
    """Return a singleton instance of RagaMusicRAG."""
    global _rag_system
    if _rag_system is None:
        _rag_system = RagaMusicRAG()
    return _rag_system

def health_check(self) -> bool:
    try:
        if self.embeddings is None:
            return False
        if self.vectorstore is None:
            return False
        self.vectorstore.similarity_search("test", k=1)
        return True
    except Exception:
        return False
