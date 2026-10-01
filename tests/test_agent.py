import pytest
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage
from pydantic import ValidationError

from main import Finding, SeverityEnum, get_base_lcel_chain


# =====================================================================
# TEST BLOCK A: MOCKING LCEL CHAINS WITH OFFLINE FAKE BACKENDS
# =====================================================================
def test_lcel_chain_logic_offline():
    # Pre-loading predictable data structures to simulate AI responses cleanly without network dependencies
    mock_response = AIMessage(content="Critical Vulnerability Exploit Fixed")
    fake_llm = FakeMessagesListChatModel(responses=[mock_response])
    
    # Generate our active production LCEL configuration pipeline structure
    testing_chain = get_base_lcel_chain(fake_llm)
    
    output = testing_chain.invoke({"vulnerability_input": "Testing local offline verification parameters."})
    
    assert isinstance(output, str)
    assert output == "Critical Vulnerability Exploit Fixed"

# =====================================================================
# TEST BLOCK B: ENFORCING STRICT PYDANTIC CONTRACT DISCREPANCIES
# =====================================================================
def test_pydantic_schema_validation_success():
    valid_payload = {
        "severity": "CRITICAL",
        "cwe_id": "CWE-89",
        "one_line_fix": "Use parameterized prepared execution statements exclusively."
    }
    validated_finding = Finding(**valid_payload)
    assert validated_finding.severity == SeverityEnum.CRITICAL
    assert validated_finding.cwe_id == "CWE-89"

def test_pydantic_schema_validation_failure():
    invalid_payload = {
        "severity": "UNKNW_SEVERITY_LEVEL_ERROR",  # Deliberate data contract violation
        "cwe_id": "CWE-79",
        "one_line_fix": "Sanitize tags"
    }
    with pytest.raises(ValidationError):
        Finding(**invalid_payload)
