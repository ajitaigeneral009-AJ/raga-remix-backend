"""
Knowledge Base Indexer for Raga Remix Studio
Converts your raga_database.py into embedded vector store
"""

import logging
from typing import List, Dict, Any
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.docstore.document import Document

from rag_config import RAGConfig
from raga_database import RAGAS, INSTRUMENTS, FUSION_STYLES, INSTRUMENT_COMPATIBILITY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RagaKnowledgeIndexer:
    """RAG system for intelligent music knowledge retrieval"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=RAGConfig.EMBEDDING_MODEL,
            openai_api_key=RAGConfig.OPENAI_API_KEY
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=RAGConfig.CHUNK_SIZE,
            chunk_overlap=RAGConfig.CHUNK_OVERLAP,
            separators=RAGConfig.SEPARATORS
        )
    
    def _create_raga_documents(self) -> List[Document]:
        """Convert RAGAS dictionary to Document objects"""
        documents = []
        
        for raga_id, raga_data in RAGAS.items():
            # Convert notes list to string for metadata
            notes_str = ', '.join(raga_data.get('notes', []))
            
            content = f"""# {raga_data.get('name', raga_id)}

**Type:** Raga (Indian Classical Music Scale)
**ID:** {raga_id}

## Musical Characteristics
**Notes (Swaras):** {notes_str}
**Time:** {raga_data.get('time', 'Any time')}
**Mood:** {raga_data.get('mood', 'Varied emotions')}
**Arohana (Ascending):** {raga_data.get('arohana', 'Standard')}
**Avarohana (Descending):** {raga_data.get('avarohana', 'Standard')}

## Key Phrases
**Pakad (Identifying Phrase):** {raga_data.get('pakad', 'Characteristic phrases')}

## Vadi and Samvadi
**Vadi (Most Prominent Note):** {raga_data.get('vadi', 'Dominant note')}
**Samvadi (Second Important Note):** {raga_data.get('samvadi', 'Consonant note')}

## Description
{raga_data.get('description', 'A classical Indian raga with unique characteristics.')}
"""
            
            doc = Document(
                page_content=content,
                metadata={
                    "type": "raga",
                    "raga_id": raga_id,
                    "name": raga_data.get('name', raga_id),
                    "time": raga_data.get('time', ''),
                    "mood": raga_data.get('mood', ''),
                    "notes": notes_str  # String, not list
                }
            )
            documents.append(doc)
        
        logger.info(f"✅ Created {len(documents)} raga documents")
        return documents
    
    def _create_instrument_documents(self) -> List[Document]:
        """Convert INSTRUMENTS dictionary to Document objects"""
        documents = []
        
        for inst_id, inst_data in INSTRUMENTS.items():
            # Get compatibility info
            compatibility_info = INSTRUMENT_COMPATIBILITY.get(inst_id, {})
            compatible_instruments = [k for k, v in compatibility_info.items() if v > 0.7]
            compatible_str = ', '.join(compatible_instruments[:5]) if compatible_instruments else 'Most instruments'
            
            # Get frequency range
            freq_range = inst_data.get('frequency_range', (0, 0))
            freq_min = freq_range[0] if isinstance(freq_range, tuple) else 0
            freq_max = freq_range[1] if isinstance(freq_range, tuple) else 0
            
            content = f"""# {inst_data.get('name', inst_id.replace('_', ' ').title())}

**Type:** Musical Instrument
**ID:** {inst_id}
**Category:** {inst_data.get('category', 'Unknown')}

## Acoustic Properties
**Frequency Range:** {freq_min}-{freq_max} Hz
**Characteristic Timbre:** {inst_data.get('characteristic_timbre', 'Unique sound')}
**Attack Type:** {inst_data.get('attack_type', 'Varies')}
**Sustain Capability:** {inst_data.get('sustain_capability', 'Moderate')}

## Fusion Suitability
**Fusion Score:** {inst_data.get('fusion_suitability', 0.5):.1%}

## Compatible Instruments
Works well with: {compatible_str}

## Description
{inst_data.get('description', 'A versatile musical instrument with unique tonal qualities.')}
"""
            
            doc = Document(
                page_content=content,
                metadata={
                    "type": "instrument",
                    "instrument_id": inst_id,
                    "name": inst_data.get('name', inst_id),
                    "category": inst_data.get('category', ''),
                    "fusion_suitability": float(inst_data.get('fusion_suitability', 0.5)),
                    "compatible_with": compatible_str  # String, not list
                }
            )
            documents.append(doc)
        
        logger.info(f"✅ Created {len(documents)} instrument documents")
        return documents
    
    def _create_fusion_style_documents(self) -> List[Document]:
        """Convert FUSION_STYLES dictionary to Document objects"""
        documents = []
        
        for style_id, style_data in FUSION_STYLES.items():
            # Extract instrument lists and convert to strings
            primary_instruments = style_data.get('primary_instruments', {})
            indian_inst = ', '.join(primary_instruments.get('indian', []))
            western_inst = ', '.join(primary_instruments.get('western', []))
            electronic_inst = ', '.join(primary_instruments.get('electronic', []))
            
            # Convert base_ragas list to string
            base_ragas_list = style_data.get('base_ragas', ['Flexible'])
            base_ragas_str = ', '.join(base_ragas_list)
            
            # Convert characteristic_features list to string
            features_list = style_data.get('characteristic_features', ['Versatile'])
            features_str = ', '.join(features_list)
            
            # Convert tempo_adjustment_range tuple to string
            tempo_range = style_data.get('tempo_adjustment_range', (0.8, 1.2))
            tempo_str = f"{tempo_range[0]}-{tempo_range[1]}"
            
            # Convert energy_progression list to string
            energy_prog = style_data.get('energy_progression', [0.3, 0.5, 0.8, 1.0])
            energy_str = ', '.join([str(x) for x in energy_prog])
            
            content = f"""# {style_data.get('name', style_id)}

**Type:** Fusion Music Style
**ID:** {style_id}

## Description
{style_data.get('description', 'A unique fusion music style.')}

## Instruments
**Indian:** {indian_inst or 'Varied'}
**Western:** {western_inst or 'Varied'}
**Electronic:** {electronic_inst or 'None'}

## Base Ragas
{base_ragas_str}

## Characteristics
**Tempo Range:** {tempo_str}
**Energy Progression:** {energy_str}

## Features
{features_str}

## Arrangement Pattern
{style_data.get('arrangement_pattern', 'Standard arrangement')}

## Mixing Style
{style_data.get('mixing_style', 'Balanced mix')}
"""
            
            doc = Document(
                page_content=content,
                metadata={
                    "type": "fusion_style",
                    "style_id": style_id,
                    "name": style_data.get('name', style_id),
                    "base_ragas": base_ragas_str,  # ✅ String, not list
                    "indian_instruments": indian_inst,  # ✅ String
                    "western_instruments": western_inst,  # ✅ String
                    "tempo_range": tempo_str,  # ✅ String
                    "features": features_str  # ✅ String
                }
            )
            documents.append(doc)
        
        logger.info(f"✅ Created {len(documents)} fusion style documents")
        return documents
    
    def create_vector_store(self):
        """Create and persist vector store from all knowledge"""
        logger.info("=" * 70)
        logger.info("🎵 Starting Raga Music Knowledge Indexing")
        logger.info("=" * 70)
        
        # Collect all documents
        all_documents = []
        all_documents.extend(self._create_raga_documents())
        all_documents.extend(self._create_instrument_documents())
        all_documents.extend(self._create_fusion_style_documents())
        
        logger.info(f"📚 Total documents to index: {len(all_documents)}")
        
        # Create vector store
        logger.info("🔄 Creating vector embeddings...")
        
        vectorstore = Chroma.from_documents(
            documents=all_documents,
            embedding=self.embeddings,
            persist_directory=RAGConfig.CHROMA_PERSIST_DIR
        )
        
        logger.info("✅ Knowledge indexing complete!")
        logger.info(f"💾 Stored in: {RAGConfig.CHROMA_PERSIST_DIR}")
        logger.info("=" * 70)
        
        return vectorstore

if __name__ == "__main__":
    indexer = RagaKnowledgeIndexer()
    indexer.create_vector_store()
