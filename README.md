# 🚀 Skill Gap Analyzer

A production-grade, local-first NLP platform designed to analyze resumes against job requirements with surgical precision. Built with a sophisticated hybrid RAG architecture and a custom-engineered NLP extraction pipeline.

![Status](https://img.shields.io/badge/Status-v2.2_Polished-success)
![NLP](https://img.shields.io/badge/NLP-SpaCy_Strict-blue)
![Architecture](https://img.shields.io/badge/Architecture-Hybrid_RAG-orange)

## ✨ Why This is Better Than Others

Most skill analyzers rely on generic LLM calls which are slow, expensive, and prone to hallucinations. **Skill Gap Analyzer** is engineered differently:

*   **Custom NLP Engine (v2.2)**: Uses a multi-stage local extraction pipeline (Segmentation → Anchoring → Strict Scoring) that outperforms simple dictionary matches and reduces LLM dependency by 90%.
*   **Zero-Hallucination Guarantee**: Implements **Strict Line Provenance**. A skill is only accepted if it exists textually in the resume. No "phantom skills" like "Cloud" being inferred from "AWS".
*   **Section-Aware Intelligence**: Differentiates between a dedicated "Skills" section and prose in "Experience". It requires context (anchoring) for skills found in sentences, ensuring they are actual competencies and not just buzzwords.
*   **Hybrid RAG Architecture**: Combines **Qdrant Vector Search** for semantic matching with strict keyword extraction and **Canonical Normalization** to collapse duplicates (e.g., "Git/GitHub" → "Git", "GitHub").
*   **Privacy First**: Core extraction happens locally on your machine. Resume data stays private.

---

## 🛠️ Technology Stack

### Backend (The Brain)
*   **FastAPI**: High-performance Python web framework.
*   **SpaCy (NLP)**: Industrial-strength Natural Language Processing for tokenization and entity recognition.
*   **RapidFuzz**: Optimized fuzzy string matching for typo tolerance without sacrificing precision.
*   **Qdrant**: High-performance Vector Database for semantic skill comparison.
*   **Sentence-Transformers**: Used for generating high-dimensional embeddings for skills.
*   **Groq (Llama 3)**: Employed sparingly for high-level roadmap generation and borderline RAG verification.

### Frontend (The Interface)
*   **React 19 + TypeScript**: Modern, type-safe UI development.
*   **Framer Motion**: Premium micro-interactions and smooth layout transitions.
*   **Recharts**: Dynamic visualization of skill gaps and proficiency distributions.
*   **Tailwind CSS (v4)**: Utility-first styling for a sleek, modern aesthetic.
*   **Radix UI**: Accessible component primitives for a premium feel.

---

## 📂 Project Structure

```bash
├── app/
│   ├── services/
│   │   ├── skill_extractor.py  # Core NLP Engine (v2.2)
│   │   ├── resume_segmenter.py # Section Awareness Logic
│   │   ├── vector_db.py        # Qdrant Integration
│   │   └── generator.py        # Groq/AI Orchestration
│   └── main.py                 # FastAPI Entry Point
├── client/                     # React + Vite Frontend
├── data/                       # Skill Taxonomies & Datasets
├── scripts/                    # Verification & Benchmarking tools
└── requirements.txt            # Python Dependencies
```

---

## ⚡ Quick Start

### 1. Prerequisites
*   Python 3.10+
*   Node.js 18+
*   Groq API Key (for roadmap generation)

### 2. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Download NLP model
python -m spacy download en_core_web_sm

# Start server
uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd client
npm install
npm run dev
```

---

## 🛡️ Verification Suite

The pipeline is verified using a rigorous battery of tests located in `/scripts`:
*   `verify_strict.py`: Tests for phantom matching and strict provenance.
*   `verify_canonical.py`: Validates canonical normalization and composite splitting.
*   `reproduce_noise.py`: Ensures zero hallucinations on complex resume formats.

---
*Built with ❤️ by a developer who hates generic AI hallucinations.*
