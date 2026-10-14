import sys
from pathlib import Path

# Force the project root directory into sys.path to guarantee import resolution on Windows
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from unittest.mock import AsyncMock, MagicMock
import pytest
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from agent_graph import build_agent_graph


@pytest.mark.anyio
async def test_agent_graph_tool_loop_offline():
    # 1. Setup Mock LLM
    mock_llm = MagicMock()
    mock_llm.bind_tools.return_value = mock_llm

    # Response 1: Model issues a tool call
    ai_tool_call_response = AIMessage(
        content="",
        tool_calls=[{
            "name": "cve_lookup",
            "args": {"cve_id": "CVE-2024-1234"},
            "id": "call_mock_id_999"
        }]
    )
    # Response 2: Model summarizes tool output
    ai_final_response = AIMessage(
        content="CVE-2024-1234 corresponds to a buffer overflow in the legacy auth module."
    )

    mock_llm.ainvoke = AsyncMock(side_effect=[ai_tool_call_response, ai_final_response])

    # 2. Compile Graph with Mock LLM
    graph = build_agent_graph(llm=mock_llm)

    # 3. Execute Graph
    initial_input = {"messages": [HumanMessage(content="Check CVE-2024-1234")]}
    final_state = await graph.ainvoke(initial_input)

    # 4. Assert State Progression
    messages = final_state["messages"]
    
    assert len(messages) == 4
    assert isinstance(messages[0], HumanMessage)
    assert isinstance(messages[1], AIMessage)
    assert len(messages[1].tool_calls) == 1
    
    # Assert tool node execution
    assert isinstance(messages[2], ToolMessage)
    assert messages[2].tool_call_id == "call_mock_id_999"
    assert "Buffer overflow" in messages[2].content

    # Assert final synthesis
    assert isinstance(messages[3], AIMessage)
    assert messages[3].content == "CVE-2024-1234 corresponds to a buffer overflow in the legacy auth module."