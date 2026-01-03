# Research: Integrated RAG Chatbot for Published Book

## Phase 0: Outline & Research

### Decision: Cohere Embedding Model Selection
**Rationale**: Using Cohere's embed-multilingual-v3.0 model for its strong performance on diverse text types and multilingual support, which is beneficial for various book content. This model provides a good balance between accuracy and cost-effectiveness for the free tier usage.
**Alternatives considered**: 
- embed-english-v3.0: Good for English-only content but less versatile
- embed-multilingual-light-v3.0: More cost-effective but potentially less accurate

### Decision: Chunk Size and Overlap Strategy
**Rationale**: Using 512-token chunks with 64-token overlap to balance context preservation and retrieval accuracy. This size allows for sufficient context while maintaining precision in retrieval. The overlap helps preserve context across chunk boundaries.
**Alternatives considered**:
- 256-token chunks: More granular but might lose context
- 1024-token chunks: More context but potentially less precise retrieval

### Decision: Vector Search Configuration in Qdrant
**Rationale**: Using HNSW indexing with ef_construct=100, M=16 for a good balance of search quality and performance. Setting top-k=5 for retrieval to provide sufficient context while avoiding information overload.
**Alternatives considered**:
- Higher ef_construct: Better accuracy but slower indexing
- Lower ef_construct: Faster indexing but potentially lower search quality

### Decision: Metadata Schema Design
**Rationale**: Storing book_id, chapter, section, and page_number as payload in Qdrant vectors to enable rich filtering and citation capabilities. This allows for precise attribution of retrieved content.
**Alternatives considered**:
- Storing only book_id: Simpler but less granular citations
- Adding sentence numbers: More granular but more complex processing

### Decision: Selected-Text Query Isolation Strategy
**Rationale**: Implementing a temporary collection approach where user-selected text is temporarily stored in a separate Qdrant collection during the query session. This ensures complete isolation from the global book index while maintaining Cohere's embedding consistency.
**Alternatives considered**:
- Filtering by metadata: Less isolated, potential for cross-contamination
- Client-side embedding: Inconsistent with Cohere-only constraint

### Decision: Context Window Size for Generation
**Rationale**: Using max 3000 tokens for context window to ensure Cohere generation remains coherent while incorporating multiple retrieved chunks. This leaves sufficient room for the query and generation.
**Alternatives considered**:
- Larger context: More information but potential for incoherence
- Smaller context: More focused but might miss important information

### Decision: Error Handling & Fallback Response Design
**Rationale**: Implementing a centralized error handler that ensures all fallback responses match the exact specification: "The provided book content does not contain sufficient information to answer this question." This guarantees consistency across all scenarios.
**Alternatives considered**:
- Multiple fallback messages: More nuanced but less consistent
- Detailed error reasons: More informative but potentially misleading

### Decision: Free-tier Performance Optimizations
**Rationale**: Implementing caching for embeddings of common chunks, connection pooling for database and vector store, and lazy loading of book content to stay within Qdrant Cloud and Neon Serverless limits.
**Alternatives considered**:
- Aggressive caching: Better performance but higher memory usage
- Pre-computed indices: Faster queries but higher storage costs

## Research Tasks Completed

1. **Cohere API Integration Patterns**
   - Researched best practices for embedding generation and management
   - Evaluated different Cohere models for RAG applications
   - Confirmed no-OpenAI constraint compliance

2. **Qdrant Cloud Free Tier Limitations**
   - Analyzed storage and query limits
   - Researched optimization strategies for free tier
   - Verified vector count and dimensionality constraints

3. **FastAPI RAG Implementation Patterns**
   - Researched async patterns for RAG systems
   - Evaluated different request/response schema designs
   - Confirmed compatibility with specification requirements

4. **Text Chunking Strategies**
   - Researched different chunking algorithms
   - Evaluated overlap strategies for context preservation
   - Confirmed deterministic chunking approaches

5. **RAG Faithfulness Validation**
   - Researched methods to ensure grounded generation
   - Evaluated hallucination detection techniques
   - Confirmed citation and attribution requirements