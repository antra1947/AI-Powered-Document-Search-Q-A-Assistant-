# streamlit_onboarding_rag_app.py
import os
import time
import streamlit as st
import dotenv

# load .env early
dotenv.load_dotenv()

# model / langchain imports
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import JsonOutputParser

# ---------------------
# Config
# ---------------------
GEMINI_MODEL = "gemini-2.5-flash-preview-09-2025"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
API_KEY = os.environ.get("GEMINI_API_KEY", "")
DATASET_FILE = "Onboarding_Dataset.md"  # must be in same folder as this script

# stable internal IDs -> human labels
DEPT_MAP = {
    "hr": "HR/Payroll",
    "it": "IT/Equipment",
    "eng": "Engineering/Tech",
    "delivery": "Delivery/Project",
    "learning": "Learning/Cert",
    "culture": "General/Culture"
}
DEPT_KEYS = list(DEPT_MAP.keys())

# ---------------------
# Pydantic schema for classification JSON
# ---------------------
class DepartmentOutput(BaseModel):
    department_id: str = Field(description=f"One of: {', '.join(DEPT_KEYS)}")

# ---------------------
# Keyword fallback classifier (quick, deterministic)
# ---------------------
KEYWORD_RULES = {
    "hr": ["payroll", "payslip", "salary", "leave", "probation", "pay"],
    "it": ["vpn", "laptop", "hardware", "install", "it helpdesk", "access", "mfa", "software"],
    "eng": ["sdk", "ide", "build", "compile", "unit test", "git", "deploy", "branch", "code"],
    "delivery": ["sprint", "standup", "delivery", "client", "project", "pm", "timeline", "deadline"],
    "learning": ["cert", "az-900", "training", "certification", "learning", "course", "study"],
}

def keyword_classify(query: str) -> str:
    q = query.lower()
    scores = {k: 0 for k in DEPT_KEYS}
    for dept, keywords in KEYWORD_RULES.items():
        for kw in keywords:
            if kw in q:
                scores[dept] += 1
    best = max(scores.items(), key=lambda x: x[1])
    if best[1] > 0:
        return best[0]
    return "culture"

# ---------------------
# Load dataset from same directory
# ---------------------
def load_local_dataset() -> str:
    if not os.path.exists(DATASET_FILE):
        st.error(f"Dataset file '{DATASET_FILE}' not found in the app folder.")
        return ""
    try:
        with open(DATASET_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        st.error(f"Failed reading dataset file: {e}")
        return ""

# ---------------------
# Cached initialization (LLM + embeddings)
# ---------------------
@st.cache_resource
def init_models(api_key: str):
    if not api_key:
        return None, None
    llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0.0, api_key=api_key)
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs={"device": "cpu"})
    return llm, embeddings

# ---------------------
# Build retriever (note leading underscore on embeddings arg to skip hashing)
# ---------------------
@st.cache_resource
def build_retriever(document_text: str, _embeddings):
    if not document_text:
        return None
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150, separators=["\n## ", "\n\n", "\n", " "])
    docs = splitter.create_documents([document_text])
    try:
        vectorstore = FAISS.from_documents(docs, _embeddings)
        return vectorstore.as_retriever(search_kwargs={"k": 3})
    except Exception as e:
        st.error(f"Indexing error: {e}")
        return None

# ---------------------
# Prompt templates
# ---------------------
CLASS_PROMPT = """
You are a strict classifier. Return ONLY valid JSON (no markdown, no explanation).

Required JSON schema:
{
  "department_id": "hr | it | eng | delivery | learning | culture"
}

Employee question:
{question}
"""

RAG_PROMPT = """
You are an Employee Onboarding AI Helper. Answer the user's question using ONLY the provided CONTEXT.

CONTEXT:
{context}

QUESTION:
{question}

If the answer is not present in the context, respond exactly: "I cannot find the answer in the provided documents."
Keep responses professional and concise.
"""

# ---------------------
# Create chains
# ---------------------
def create_classification_chain(llm):
    template = ChatPromptTemplate.from_template(CLASS_PROMPT)
    parser = JsonOutputParser(pydantic_object=DepartmentOutput)
    # prompt -> llm -> parser
    chain = (template | llm | parser)
    return chain

def create_rag_chain(llm, retriever):
    rag_template = ChatPromptTemplate.from_template(RAG_PROMPT)
    def fmt(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    rag_chain = ({"context": retriever | RunnableLambda(fmt), "question": RunnablePassthrough()} | rag_template | llm)
    return rag_chain

# ---------------------
# Streamlit UI
# ---------------------
def main():
    st.set_page_config(page_title="Employee Onboarding RAG Helper", layout="wide")
    st.title("Employee Onboarding RAG Helper")
    st.markdown("Ask onboarding questions. Answers are grounded in the local `Onboarding_Dataset.md` file.")

    # debug toggle
    debug = st.sidebar.checkbox("Show debug info", value=False)

    # Status / metadata
    st.sidebar.header("System")
    st.sidebar.markdown(f"**LLM:** {GEMINI_MODEL}")
    st.sidebar.markdown(f"**Embeddings:** {EMBEDDING_MODEL_NAME}")
    st.sidebar.markdown(f"**Dataset file:** {DATASET_FILE}")
    if not API_KEY:
        st.sidebar.error("GEMINI_API_KEY missing. Put it in .env")

    # Load dataset
    dataset_text = load_local_dataset()
    if not dataset_text:
        st.stop()

    # Init models
    llm, embeddings = init_models(API_KEY)
    if llm is None or embeddings is None:
        st.error("LLM or embeddings initialization failed. Check GEMINI_API_KEY and dependencies.")
        st.stop()

    # Build retriever (embeddings argument intentionally named with leading underscore)
    retriever = build_retriever(dataset_text, embeddings)
    if retriever is None:
        st.error("Failed to build retriever / index.")
        st.stop()

    # Create chains in session state for responsiveness
    if "classification_chain" not in st.session_state:
        st.session_state["classification_chain"] = create_classification_chain(llm)
    if "rag_chain" not in st.session_state:
        st.session_state["rag_chain"] = create_rag_chain(llm, retriever)

    st.text("Enter a question below and press Get Answer.")
    q = st.text_area("Your question:", height=140, placeholder="e.g., How do I request a laptop? Is Saturday mandatory?")

    if st.button("Get Answer"):
        if not q.strip():
            st.warning("Please type a question.")
        else:
            start = time.time()
            # 1) Try strict LLM classification -> parsed JSON
            classification_chain = st.session_state["classification_chain"]
            dept_key = None
            raw_class_output = None
            parser_failed = False

            try:
                parsed = classification_chain.invoke({"question": q})
                # parsed should be a dict-like with department_id
                raw_class_output = parsed
                dept_candidate = parsed.get("department_id", "").strip().lower()
                if dept_candidate in DEPT_MAP:
                    dept_key = dept_candidate
            except Exception as e:
                parser_failed = True
                if debug:
                    st.warning(f"Classification parser error: {e}")

            # 2) fallback to keyword if parser failed or returned invalid key
            if dept_key is None:
                dept_key = keyword_classify(q)
                fallback_used = True
            else:
                fallback_used = False

            dept_label = DEPT_MAP.get(dept_key, "General/Culture")

            # 3) Run RAG chain
            rag_chain = st.session_state["rag_chain"]
            try:
                response = rag_chain.invoke(q)
                answer = response.content
            except Exception as e:
                answer = f"RAG chain error: {e}"

            elapsed = time.time() - start

            # Display
            st.subheader("Routing")
            st.markdown(f"- **Internal id:** `{dept_key}`  \n- **Department:** **{dept_label}**")
            if fallback_used:
                st.info("Classifier fallback used: keyword rules applied because strict JSON parsing failed.")
            st.subheader("Answer (grounded)")
            st.info(answer)
            st.caption(f"Time taken: {elapsed:.2f} s")

            if debug:
                st.subheader("Debug info")
                st.json({
                    "raw_class_output": raw_class_output,
                    "parser_failed": parser_failed,
                    "dept_key_used": dept_key,
                    "dept_label": dept_label,
                    "fallback_used": fallback_used
                })

if __name__ == "__main__":
    main()
