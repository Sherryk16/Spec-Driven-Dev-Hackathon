---
sidebar_position: 6
---

# Research & Decisions

This document records the decisions made for key technical clarifications during the planning phase of fea
ture `002-ros2-module-1`.

---

## 1. Docusaurus Chatbot UI Integration

- **Need**: A method to embed the React-based RAG chatbot UI into the Docusaurus site.
- **Decision**: A custom, local Docusaurus plugin will be created.
- **Rationale**:
  - Docusaurus has a well-defined plugin architecture that allows for adding custom functionality.        
  - Using the `clientModules` option within a custom plugin is the standard and recommended way to inject 
a global React component, such as a floating chat widget.
  - This approach avoids the need for external, third-party plugins which may not be maintained or offer t
he required flexibility. It gives us full control over the chatbot's appearance, behavior, and integration
 with our backend.
- **Alternatives Considered**:
  - **Swizzling Docusaurus theme components**: This involves ejecting a core theme component (like the `La
yout` or `Footer`) and manually adding the chatbot component. This is more complex and creates a maintenan
ce burden, as we would be responsible for keeping the swizzled component up-to-date with Docusaurus upgrad
es.
  - **Using a pre-made plugin**: A search did not reveal any standard, "drop-in" plugins that were specifi
cally designed for a custom RAG backend and offered the desired level of control.

---

## 2. FastAPI Backend Deployment

- **Need**: A hosting platform for the Python-based FastAPI backend.
- **Decision**: Render.
- **Rationale**:
  - Render offers a free tier for web services that includes 750 hours of runtime per month, which is enou
gh to run the service continuously.
  - While the service "spins down" after 15 minutes of inactivity, this is an acceptable trade-off for a f
ree, persistent hosting solution. The initial "cold start" delay is not critical for this project's use ca
se.
  - The constitution specifies using Neon for the database, so Render's expiring free-tier database is not
 a concern.
- **Alternatives Considered**:
  - **Railway**: Railway's free tier is a one-time $5 credit that expires after 30 days. This makes it mor
e of a temporary trial than a sustainable free hosting option, making it unsuitable for this project.     
  - **Serverless (e.g., AWS Lambda, Vercel Serverless Functions)**: While a valid option, setting up a ful
l FastAPI application in a serverless environment can be more complex than deploying to a platform-as-a-se
rvice like Render. Given the straightforward nature of the API, the simplicity of Render is preferred.    

---

## 3. RAG Embedding Model and Chunking Strategy

- **Need**: A strategy for converting the book's text into vector embeddings for retrieval.
- **Decision**:
  - **Embedding Model**: OpenAI `text-embedding-3-small`.
  - **Chunking Strategy**: A hybrid approach combining structural and recursive methods.
- **Rationale**:
  - **Model**: `text-embedding-3-small` provides a strong balance of high performance on semantic search t
asks and cost-effectiveness, making it ideal for this project. It is a well-supported and powerful general
-purpose model capable of handling technical documentation.
  - **Chunking**: Technical documentation has inherent structure.
    1.  **Structural Splitting**: We will first split documents by their Markdown headers (`##`, `###`, et
c.) and self-contained code blocks. This keeps logically related content together.
    2.  **Recursive Splitting**: For any structurally-derived chunk that exceeds the model's token limit, 
we will apply recursive character splitting with a small token overlap (~100 tokens). This breaks down lar
ge sections while trying to preserve sentence and paragraph context.
    3.  **Metadata**: Each vector will be stored with metadata (source file, chapter, section title) to en
able citations and more precise context retrieval.
- **Alternatives Considered**:
  - **Different Models**: Models like `E5-large-v2` or `BGE-large-en` are strong performers but may requir
e more setup to host and use. OpenAI's API is simpler to integrate for this project. `text-embedding-3-lar
ge` offers higher accuracy but at a higher cost. `small` is sufficient for this application.
  - **Simpler Chunking**: A fixed-size chunking strategy is easier to implement but is ignorant of the doc
ument's structure. It often splits sentences, code blocks, or paragraphs, leading to a loss of context and
 lower-quality retrieval.

---

## 4. Vector Database

- **Need**: A database to store the text embeddings for similarity search.
- **Decision**: Qdrant Cloud (Free Tier).
- **Rationale**: This is mandated by the project constitution. Qdrant is a specialized vector database bui
lt for performance and scalability, and its free cloud tier is sufficient for the project's scale.        
- **Alternatives Considered**: None, as the choice is fixed by the project's governing document.
