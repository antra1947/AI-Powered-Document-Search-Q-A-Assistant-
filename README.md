# AI-Powered Document Search & Q&A Assistant

Built by **Antra** — a GenAI-powered assistant that helps new hires get instant answers about HR policies, IT setup, engineering practices, agile delivery, learning paths, and company culture. Answers are grounded strictly in your organization's onboarding documents using **Retrieval-Augmented Generation (RAG)**.

Built with **Streamlit**, **LangChain**, **Google Gemini**, **HuggingFace Sentence Transformers**, and **FAISS**.

---

## What Makes It Interesting

- **Hybrid classifier** — an LLM classifier outputs strict JSON to route each question into one of six departments (HR/Payroll, IT/Equipment, Engineering, Delivery, Learning, Culture). If JSON parsing fails, a deterministic keyword-rule fallback kicks in — so the app stays stable even on a bad model response.
- **Hallucination-free answers** — the RAG prompt instructs the LLM to answer *only* from retrieved context. If the answer isn't there, it says so clearly instead of making something up.
- **FAISS vector store** — documents are chunked via `RecursiveCharacterTextSplitter` (chunk size 1000, overlap 150) and embedded using `sentence-transformers/all-MiniLM-L6-v2` — lightweight enough to run on CPU.
- **Debug panel** — a toggleable sidebar exposes the classifier's raw output, parser failures, and whether fallback was used. Handy for evaluating routing quality.
- **Cached resources** — `@st.cache_resource` keeps model and index loading fast across reruns.

---

## Architecture

```
        ┌────────────────────┐
        │   User question    │
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────┐       ┌────────────────────┐
        │ LLM Classifier     │──fail►│ Keyword fallback   │
        │ (strict JSON)      │       │ (deterministic)    │
        └─────────┬──────────┘       └─────────┬──────────┘
                  │                            │
                  ▼                            ▼
              ┌────────────────────────────────────┐
              │  Department label (hr/it/eng/...)  │
              └──────────────────┬─────────────────┘
                                 │
                       ┌─────────▼──────────┐
                       │  FAISS Retriever   │
                       │  (top-k = 3)       │
                       └─────────┬──────────┘
                                 │
                       ┌─────────▼──────────┐
                       │  Grounded LLM      │
                       │  (Gemini)          │
                       └─────────┬──────────┘
                                 │
                       ┌─────────▼──────────┐
                       │  Final answer      │
                       └────────────────────┘
```

---

## Tech Stack

| Layer | Tooling |
|---|---|
| LLM | Google Gemini (`gemini-2.5-flash-preview-09-2025`) via `langchain-google-genai` |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (HuggingFace, CPU) |
| Vector store | FAISS |
| Chunking | LangChain `RecursiveCharacterTextSplitter` |
| Validation | Pydantic v2 (strict JSON schema for classifier output) |
| UI | Streamlit |

---

## Project Structure

```
.
├── app.py                   # Main Streamlit app
├── Onboarding_Dataset.md    # Knowledge base used for RAG
├── sample_questions.txt     # Sample queries to test with
├── requirements.txt
├── .env.example             # Copy to .env and add your GEMINI_API_KEY
└── README.md
```

---

## Setup

```powershell
git clone https://github.com/antra1947/AI-Powered-Document-Search-Q-A-Assistant-.git
cd AI-Powered-Document-Search-Q-A-Assistant-

python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Copy-Item .env.example .env
# Open .env and paste your GEMINI_API_KEY (get one at https://aistudio.google.com/app/apikey)
```

---

## Run

```powershell
streamlit run app.py
```

Once the app opens in your browser, paste a question from `sample_questions.txt` or type your own. You'll get:
- the department the classifier routed it to
- whether keyword fallback was triggered
- a grounded answer from the knowledge base
- raw classifier output (if debug mode is on)

---

## Notes

- `Onboarding_Dataset.md` is a sample knowledge base for a fictional company. Swap it out with your own onboarding docs to adapt this for any organization.
- Casual greetings like "hi" or "thanks" are short-circuited and skip the RAG pipeline entirely.
