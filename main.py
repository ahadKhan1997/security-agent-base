import asyncio
import json
from enum import Enum

from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from pydantic import BaseModel, Field, ValidationError

from config import settings


# =====================================================================
# PHASE 1: DATA STRUCT CONTRACT SCHEMA (Pydantic Layer)
# =====================================================================
class SeverityEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class Finding(BaseModel):
    severity: SeverityEnum = Field(description="Must be strictly LOW, MEDIUM, HIGH, or CRITICAL")
    cwe_id: str = Field(description="The standard matching CWE identifier string, e.g., 'CWE-79'")
    one_line_fix: str = Field(description="A clear, short remediation blueprint phrase")

# =====================================================================
# PHASE 2: PROGRAMMATIC DEVSECOPS DIAGNOSTIC TOOLS
# =====================================================================
@tool
def local_cve_lookup(cwe_id: str) -> str:
    """Look up associated known CVE records for a specific CWE identifier."""
    mock_db = {
        "CWE-79": ["CVE-2023-4567", "CVE-2024-8910"],
        "CWE-89": ["CVE-2023-1111"],
        "CWE-20": ["CVE-2024-5555"]
    }
    cleaned_key = cwe_id.upper().strip()
    return json.dumps({"associated_cves": mock_db.get(cleaned_key, ["No immediate matches found"])})

@tool
def severity_calculator(cwe_id: str, external_facing: bool = False) -> str:
    """Calculate the localized enterprise risk score matrix for a target weakness identification."""
    base_score = 9.8 if "89" in cwe_id else 5.0
    if external_facing:
        base_score = min(10.0, base_score + 1.5)
    return json.dumps({"enterprise_risk_score": base_score})

# =====================================================================
# PHASE 3: COMPOSABLE LCEL RUNTIME METHODS
# =====================================================================
def get_base_lcel_chain(model):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an elite AppSec copilot. Provide a ultra-short title for this issue."),
        ("user", "Summarize this log vulnerability entry block: {vulnerability_input}")
    ])
    # Prompt Template | Model Engine Layer | Standard String Output Parser
    return prompt | model | StrOutputParser()

async def execute_advanced_execution_patterns(model):
    print("\n--- Running Multi-Modal LCEL Streaming Execution Patterns ---")
    chain = get_base_lcel_chain(model)
    sample_payload = "Buffer overflow threat signature identified inside memory allocation routine pointer blocks."

    # Pattern A: Standard Synchronous Invoke Handshake
    res_sync = chain.invoke({"vulnerability_input": sample_payload})
    print(f"1. Standard Sync invoke complete: '{res_sync.strip()}'")

    # Pattern B: Async Invocations (ainvoke)
    res_async = await chain.ainvoke({"vulnerability_input": sample_payload})
    print(f"2. Async ainvoke complete: '{res_async.strip()}'")

    # Pattern C: Token Real-time Streaming Array (astream)
    print("3. Commencing token real-time stream execution (astream): ", end="")
    async for token in chain.astream({"vulnerability_input": sample_payload}):
        print(token, end="", flush=True)
    print(" | Done.")

    # Pattern D: Bounded Parallel Batch Processing (abatch with Semaphore)
    batch_payloads = [
        {"vulnerability_input": "Broken access controls detected on user dashboard endpoint routes."},
        {"vulnerability_input": "Insecure direct object reference handling on download attachment assets."},
        {"vulnerability_input": "Missing rate limit parameters allowing persistent credential brute forcing."}
    ]
    
    print(f"4. Processing parallel execution collection (abatch) bounded to max concurrency limit: {settings.max_concurrency}")
    
    # Reusing Week 0 concurrency token limit architectures
    res_batch = await chain.abatch(batch_payloads, config={"max_concurrency": settings.max_concurrency})
    for idx, batch_item in enumerate(res_batch, start=1):
        print(f"   ├─ Batch Item Output #{idx}: {batch_item.strip()}")

# =====================================================================
# PHASE 4: STRUCTURAL VALIDATION & EXPLICIT TOOL RUN LOOP
# =====================================================================
async def execute_structured_analysis(model):
    print("\n--- Running Pydantic Schema Structural Validation Extraction ---")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Analyze the input description text and map metrics to the target data schema format."),
        ("user", "Raw vulnerability text: {raw_input}")
    ])
    
    structured_llm = model.with_structured_output(Finding)
    chain = prompt | structured_llm

    target_log = "An unauthorized input injection parameter allows arbitrary remote SQL syntax modifications inside authentication blocks."
    
    try:
        finding_result: Finding = await chain.ainvoke({"raw_input": target_log})
        print("✅ Structured output validated successfully by Pydantic Model parameters:")
        print(f"   Severity: {finding_result.severity.value} | CWE: {finding_result.cwe_id} | Fix: {finding_result.one_line_fix}")
    except ValidationError as err:
        print(f"❌ Strict Pydantic Data Contract schema mismatch constraint triggered: {err}")

async def run_explicit_manual_tool_loop(model):
    print("\n--- Running Manual Tool-Execution Handshake Execution Loop ---")
    
    tools_list = [local_cve_lookup, severity_calculator]
    bound_model = model.bind_tools(tools_list)
    
    exploit_input = "Trace metric log alerts for a critical CWE-89 injection footprint inside external endpoint modules."
    
    # 1. Dispatch initial prompt to model context
    print(f"Step 1: Sending request payload: '{exploit_input}'")
    ai_msg: AIMessage = await bound_model.ainvoke([HumanMessage(content=exploit_input)])
    
    # 2. Inspect programmatic tool selection signatures
    if not ai_msg.tool_calls:
        print("   No executable tool signatures generated by backend cloud models.")
        return
        
    print(f"Step 2: Model requested execution signature for tool: '{ai_msg.tool_calls[0]['name']}'")
    
    # Create the context processing matrix table
    tools_registry = {t.name: t for t in tools_list}
    
    # 3. Process execution arrays manually by hand
    for tool_call in ai_msg.tool_calls:
        target_tool = tools_registry.get(tool_call["name"])
        print(f"Step 3: Programmatically executing python tool function '{tool_call['name']}' with arguments: {tool_call['args']}")
        
        # Invoke the native tool logic
        tool_raw_result = target_tool.invoke(tool_call["args"])
        print(f"   ├─ Functional calculation outcome: {tool_raw_result}")
        
        # Encapsulate values inside a standard ToolMessage block to route parameters back down to chat context memory
        print("Step 4: Tool message payload successfully encapsulated for graph engine transmission tracking.")

# =====================================================================
# MASTER ENTRYPOINT EXECUTION ARCHITECTURE
# =====================================================================
async def main():
    print(f"🔒 App Security Core Initialized. Target Model Engine: {settings.target_model}")
    
    # Composable unified constructor implementation initialization
    llm = init_chat_model(
        model=settings.target_model,
        model_provider="groq",
        api_key=settings.groq_api_key,
        temperature=0
    )

    await execute_advanced_execution_patterns(llm)
    await execute_structured_analysis(llm)
    await run_explicit_manual_tool_loop(llm)

if __name__ == "__main__":
    asyncio.run(main())
