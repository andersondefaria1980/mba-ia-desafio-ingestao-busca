import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

def ingest_pdf():
    PDF_PATH = os.getenv("PDF_PATH")    
    current_dir = Path(__file__).parent.parent    
    pdf_path = current_dir / PDF_PATH    
    docs = PyPDFLoader(str(pdf_path)).load()
    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150,
        add_start_index=False).split_documents(docs)
    if not splits:
        raise SystemExit(0)
    enriched = [
    Document(
        page_content=d.page_content,
        metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
    )
    for d in splits
    ]
    ids = [f"doc-{i}" for i in range(len(enriched))]
    embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLEAI_MODEL","gemini-embedding-001"))
    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PGVECTOR_COLLECTION"),
        connection=os.getenv("PGVECTOR_URL"),
        use_jsonb=True,
    )
    store.add_documents(documents=enriched, ids=ids)


if __name__ == "__main__":
    ingest_pdf()