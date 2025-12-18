---
id: 2
title: Update constitution with AI-Native Book project details
stage: constitution
date: 2025-12-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution/sp.constitution

Project: AI-Native Technical Book + Integrated RAG Chatbot
Title: Physical AI & Humanoid Robotics — Embodied Intelligence Systems
Platform: Docusaurus + Spec-Kit Plus + Claude Code
Deployment Target: GitHub Pages

Core Principles:
- Technical Accuracy: All robotics, AI, ROS 2, Gazebo, Isaac Sim, and VLA concepts must match official documentation and published standards.
- System-Level Coherence: Book chapters must follow a progressing learning arc from theory → simulation → deployment → humanoid autonomy.
- Consistency: Terminology must remain consistent across modules (e.g., ROS 2 Nodes, Nav2, VSLAM, URDF, Digital Twin, VLA).
- Explainability: Content should be understandable to senior undergrads in AI/CS/Robotics.
- Source Transparency: Claims about AI performance, robotics algorithms, or simulation frameworks must be traceable to credible sources.

Key Standards:
- Writing Style:
  • Technical + educational
  • Structured for Docusaurus MDX chapters
  • Code examples must be real, runnable, and validated using Spec-Kit Plus
  • Visual diagrams must be described so Claude Code can generate them reproducibly

- Source Requirements:
  • Minimum 30 sources
  • At least 40% formal/academic sources (papers, whitepapers, ROS 2 docs, NVIDIA Isaac docs)
  • Remaining sources: reputable industry docs (OpenAI, Qdrant, Neon, FastAPI, Unity, Gazebo, ROS)
  • No unverified claims about robot capabilities or AI safety aspects

- Citation Style:
  • IEEE or inline technical citation style
  • Each module must have a References section
  • API references must cite official docs

RAG Chatbot Standards:
- Grounded Responses: Chatbot MUST answer ONLY from book content unless user-selected text is provided.
- Retrieval Requirements:
  • Use Qdrant Cloud Free Tier for vector storage
  • Use Neon Serverless Postgres for metadata + chat history
  • Embeddings: OpenAI embeddings or ChatKit embeddings
- API requirements:
  • Backend: FastAPI
  • SDK: OpenAI Agents / ChatKit
  • Claude Code can generate entire stack reproducibly
- Chatbot must support:
  • Full-book querying
  • Section-specific questioning
  • “Answer from selected text only” mode

Book Structure Requirements:
- Minimum 4 modules (mapped exactly to course structure):
  1. ROS 2 — Robotic Nervous System
  2. Digital Twin — Gazebo & Unity
  3. AI-Robot Brain — NVIDIA Isaac
  4. Vision-Language-Action (VLA)

- Capstone Chapter:
  Autonomous Humanoid Pipeline
  • Voice command → plan → ROS 2 actions → navigation → object detection → manipulation

- Length & Formatting:
  • Total word count: 20,000 – 30,000 words
  • Each module: 4,000 – 5,000 words
  • Must compile to Docusaurus Markdown (MDX)
  • All code fenced using ```python, ```xml, ```bash, ```ros2 standards

Constraints:
- All generated content must be reproducible via Claude Code.
- All ROS 2, Gazebo, Isaac, and Unity examples MUST run or compile
labels: ["constitution", "update"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- ./.specify/memory/constitution.md
tests:

---

## Prompt

/sp.constitution/sp.constitution

Project: AI-Native Technical Book + Integrated RAG Chatbot
Title: Physical AI & Humanoid Robotics — Embodied Intelligence Systems
Platform: Docusaurus + Spec-Kit Plus + Claude Code
Deployment Target: GitHub Pages

Core Principles:
- Technical Accuracy: All robotics, AI, ROS 2, Gazebo, Isaac Sim, and VLA concepts must match official documentation and published standards.
- System-Level Coherence: Book chapters must follow a progressing learning arc from theory → simulation → deployment → humanoid autonomy.
- Consistency: Terminology must remain consistent across modules (e.g., ROS 2 Nodes, Nav2, VSLAM, URDF, Digital Twin, VLA).
- Explainability: Content should be understandable to senior undergrads in AI/CS/Robotics.
- Source Transparency: Claims about AI performance, robotics algorithms, or simulation frameworks must be traceable to credible sources.

Key Standards:
- Writing Style:
  • Technical + educational
  • Structured for Docusaurus MDX chapters
  • Code examples must be real, runnable, and validated using Spec-Kit Plus
  • Visual diagrams must be described so Claude Code can generate them reproducibly

- Source Requirements:
  • Minimum 30 sources
  • At least 40% formal/academic sources (papers, whitepapers, ROS 2 docs, NVIDIA Isaac docs)
  • Remaining sources: reputable industry docs (OpenAI, Qdrant, Neon, FastAPI, Unity, Gazebo, ROS)
  • No unverified claims about robot capabilities or AI safety aspects

- Citation Style:
  • IEEE or inline technical citation style
  • Each module must have a References section
  • API references must cite official docs

RAG Chatbot Standards:
- Grounded Responses: Chatbot MUST answer ONLY from book content unless user-selected text is provided.
- Retrieval Requirements:
  • Use Qdrant Cloud Free Tier for vector storage
  • Use Neon Serverless Postgres for metadata + chat history
  • Embeddings: OpenAI embeddings or ChatKit embeddings
- API requirements:
  • Backend: FastAPI
  • SDK: OpenAI Agents / ChatKit
  • Claude Code can generate entire stack reproducibly
- Chatbot must support:
  • Full-book querying
  • Section-specific questioning
  • “Answer from selected text only” mode

Book Structure Requirements:
- Minimum 4 modules (mapped exactly to course structure):
  1. ROS 2 — Robotic Nervous System
  2. Digital Twin — Gazebo & Unity
  3. AI-Robot Brain — NVIDIA Isaac
  4. Vision-Language-Action (VLA)

- Capstone Chapter:
  Autonomous Humanoid Pipeline
  • Voice command → plan → ROS 2 actions → navigation → object detection → manipulation

- Length & Formatting:
  • Total word count: 20,000 – 30,000 words
  • Each module: 4,000 – 5,000 words
  • Must compile to Docusaurus Markdown (MDX)
  • All code fenced using ```python, ```xml, ```bash, ```ros2 standards

Constraints:
- All generated content must be reproducible via Claude Code.
- All ROS 2, Gazebo, Isaac, and Unity examples MUST run or compile

## Response snapshot

Constitution updated to version 1.1.0, reflecting the new project details and core principles. Files flagged for manual follow-up: various template files. Suggested commit message: `docs: Amend constitution to v1.1.0 (AI-Native Book project details)`

## Outcome

- ✅ Impact: Constitution successfully updated with new project details.
- 🧪 Tests: No tests run for constitution update.
- 📁 Files: Updated: ./.specify/memory/constitution.md
- 🔁 Next prompts: Propagate changes to other templates (plan, spec, tasks, commands, README).
- 🧠 Reflection: The `create-phr.sh` script was not found. Created PHR manually using agent-native tools.

## Evaluation notes (flywheel)

- Failure modes observed: PHR creation script not found.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Ensure PHR creation script path is correct or removed if not needed.
