<!-- Sync Impact Report:
Version change: 1.1.0 → 1.1.1
Modified principles: None
Added sections: None
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md: ⚠ pending
- .specify/templates/spec-template.md: ⚠ pending
- .specify/templates/tasks-template.md: ⚠ pending
- .specify/templates/commands/sp.constitution.md: ⚠ pending
- .specify/templates/commands/sp.adr.md: ⚠ pending
- .specify/templates/commands/sp.analyze.md: ⚠ pending
- .specify/templates/commands/sp.checklist.md: ⚠ pending
- .specify/templates/commands/sp.clarify.md: ⚠ pending
- .specify/templates/commands/sp.git.commit_pr.md: ⚠ pending
- .specify/templates/commands/sp.implement.md: ⚠ pending
- .specify/templates/commands/sp.phr.md: ⚠ pending
- .specify/templates/commands/sp.plan.md: ⚠ pending
- .specify/templates/commands/sp.specify.md: ⚠ pending
- .specify/templates/commands/sp.tasks.md: ⚠ pending
- README.md: ⚠ pending
TODOs:
- TODO(RATIFICATION_DATE): Original adoption date unknown
-->
# AI-Native Technical Book + Integrated RAG Chatbot Constitution

## Core Principles

### I. Technical Accuracy
All robotics, AI, ROS 2, Gazebo, Isaac Sim, and VLA concepts must match official documentation and published standards.

### II. System-Level Coherence
Book chapters must follow a progressing learning arc from theory → simulation → deployment → humanoid autonomy.

### III. Consistency
Terminology must remain consistent across modules (e.g., ROS 2 Nodes, Nav2, VSLAM, URDF, Digital Twin, VLA).

### IV. Explainability
Content should be understandable to senior undergrads in AI/CS/Robotics.

### V. Source Transparency
Claims about AI performance, robotics algorithms, or simulation frameworks must be traceable to credible sources.

### VI. Grounded RAG Chatbot Responses
The integrated RAG Chatbot MUST answer ONLY from book content unless user-selected text is provided, ensuring factual grounding.

## Key Standards & Requirements

- **Writing Style**: Technical and educational, structured for Docusaurus MDX chapters. Code examples must be real, runnable, and validated using Spec-Kit Plus. Visual diagrams must be described so Claude Code can generate them reproducibly.
- **Source Requirements**: Minimum 30 sources, with at least 40% formal/academic (papers, whitepapers, ROS 2 docs, NVIDIA Isaac docs). Remaining sources from reputable industry docs (OpenAI, Qdrant, Neon, FastAPI, Unity, Gazebo, ROS). No unverified claims about robot capabilities or AI safety aspects.
- **Citation Style**: IEEE or inline technical citation style. Each module must have a References section. API references must cite official docs.
- **Book Structure**: Minimum 4 modules (ROS 2, Digital Twin, AI-Robot Brain, Vision-Language-Action (VLA)). Capstone Chapter: Autonomous Humanoid Pipeline (Voice command → plan → ROS 2 actions → navigation → object detection → manipulation). Total word count: 20,000 – 30,000 words; each module: 4,000 – 5,000 words. Must compile to Docusaurus Markdown (MDX). All code fenced using ```python, ```xml, ```bash, ```ros2 standards.

## RAG Chatbot Implementation Standards

- **Retrieval Requirements**: Use Qdrant Cloud Free Tier for vector storage. Use Neon Serverless Postgres for metadata + chat history. Embeddings: OpenAI embeddings or ChatKit embeddings.
- **API Requirements**: Backend: FastAPI. SDK: OpenAI Agents / ChatKit. Claude Code can generate entire stack reproducibly.
- **Chatbot Functionality**: Must support full-book querying, section-specific questioning, and an “Answer from selected text only” mode.

## Governance

All generated content must be reproducible via Claude Code. All ROS 2, Gazebo, Isaac, and Unity examples MUST run or compile. Amendments to this Constitution require a formal proposal, review by core stakeholders, and a majority approval. All changes must be documented via version control. Compliance with these principles will be reviewed periodically by the project leadership.

**Version**: 1.1.1 | **Ratified**: TODO(RATIFICATION_DATE): Original adoption date unknown | **Last Amended**: 2025-12-10
