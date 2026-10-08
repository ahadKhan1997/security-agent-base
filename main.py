import asyncio
import hashlib
from sqlalchemy.ext.asyncio import create_async_engine
from langchain_postgres.vectorstores import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chat_models import init_chat_model
from config import settings

# =====================================================================
# PHASE 1: COMPUTE CONTEXT-AWARE STABLE CHUNKS
# =====================================================================
def get_document_chunks() -> list[Document]:
    """Simulates local file ingestion and splits text payload into chunks."""
    raw_lines = [
        "DEVMETRIC-POLICY-01: All production multi-stage container builds must omit debugging utilities.",
        "DEVMETRIC-POLICY-02: Secret detection hooks like Gitleaks must run during pre-merge staging pull loops.",
        "DEVMETRIC-POLICY-03: Container base OS layers must run vulnerability scanning routines weekly via Trivy."
    ]
    
    documents = []
    for line in raw_lines:
        chunk_id = hashlib.sha256(line.encode("utf-8")).hexdigest()[:16]
        doc = Document(
            page_content=line,
            metadata={"source": "data/security_blueprint.txt", "chunk_id": chunk_id}
        )
        documents.append(doc)
    return documents

# =====================================================================
# PHASE 2: FORMAT RETRIEVED CONTEXT FORMATTERS
# =====================================================================
def format_docs(docs: list[Document]) -> str:
    """Combines text sections extracted from pgvector to build prompt context."""
    return "\n\n".join([f"[Source: {doc.metadata.get('source')}] {doc.page_content}" for doc in docs])

# =====================================================================
# PHASE 3: MASTER ENGINE RUNTIME EXECUTION LINK
# =====================================================================
async def main():
    print("🔒 Initializing Bounded Week 2 Async RAG Architecture Context Array...")
    
    # 1. Initialize local HuggingFace embedding layer
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 2. Build the explicit async driver connection string mapping
    # Note: langchain-postgres modern async engine requires 'postgresql+psycopg://'
    async_connection_string = settings.adjusted_db_url.replace("postgresql://", "postgresql+psycopg://")
    
    # Create a native, persistent async database engine pool
    async_engine = create_async_engine(
        async_connection_string, 
        pool_pre_ping=True,
        connect_args={"connect_timeout": 10}
    )
    
    # Instantiate the Postgres vector store engine container connection using the async engine
    vector_store = PGVector(
        embeddings=embeddings,
        connection=async_engine, # Explicitly pass the active async engine pool
        collection_name="cybersec_policies",
        use_jsonb=True
    )
    
    # Ingest data with deterministic IDs to avoid data ingestion bloat
    chunks = get_document_chunks()
    stable_ids = [doc.metadata["chunk_id"] for doc in chunks]
    
    print(f"📥 Loading {len(chunks)} structural documents into pgvector indices...")
    await vector_store.aadd_documents(documents=chunks, ids=stable_ids)
    
    # 3. Initialize the unified Groq model provider client config
    llm = init_chat_model(
        model=settings.target_model,
        model_provider="groq",
        api_key=settings.groq_api_key,
        temperature=0
    )
    
    # 4. Construct the Grounded RAG Prompt Template
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert DevSecOps audit compliance advisor.\n"
            "Answer the user query strictly utilizing the trusted knowledge context provided below.\n"
            "If the answer cannot be found in the context, say 'I cannot locate policy details.'\n\n"
            "Trusted Context:\n{context}"
        )),
        ("user", "{question}")
    ])
    
    # 5. Build Composable LCEL Retrieval Chain Array
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    
    rag_chain = (
        {
            "context": retriever | format_docs, 
            "question": RunnablePassthrough()
        }
        | prompt 
        | llm 
        | StrOutputParser()
    )
    
    # 6. Execute live grounded query tracking execution
    user_query = "What is the explicit policy metric constraint regarding Gitleaks secret hooks?"
    print(f"\n🔍 Querying Database Engine: '{user_query}'")
    
    retrieved_source_chunks = await retriever.ainvoke(user_query)
    ai_response = await rag_chain.ainvoke(user_query)
    
    print("\n🏆 Grounded Response Metrics Returned:")
    print(f" ├─ Answer: {ai_response.strip()}")
    print(" └─ Verified Source Attributes:")
    for chunk in retrieved_source_chunks:
        print(f"    • [{chunk.metadata.get('chunk_id')}] -> {chunk.page_content}")

    # Cleanly close down the asynchronous engine pool on completion
    await async_engine.dispose()

if __name__ == "__main__":
    import sys
    import selectors
    
    # 🛡️ Windows Event Loop Override Pattern
    if sys.platform == "win32":
        loop_factory = lambda: asyncio.SelectorEventLoop(selectors.SelectSelector())
        asyncio.run(main(), loop_factory=loop_factory)
    else:
        asyncio.run(main())
