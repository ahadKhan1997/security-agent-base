import pytest
from langchain_core.documents import Document
from main import format_docs

def test_document_context_formatter_output():
    """Asserts that retrieved database documents are formatted correctly for prompt context injection."""
    sample_docs = [
        Document(page_content="DEVMETRIC-POLICY-01: Rule Test Alpha", metadata={"source": "test_file.txt"}),
        Document(page_content="DEVMETRIC-POLICY-02: Rule Test Beta", metadata={"source": "test_file.txt"})
    ]
    
    # Execute your native Week 2 utility function
    output_context = format_docs(sample_docs)
    
    # Verify the formatting contract is maintained
    assert "[Source: test_file.txt] DEVMETRIC-POLICY-01: Rule Test Alpha" in output_context
    assert "[Source: test_file.txt] DEVMETRIC-POLICY-02: Rule Test Beta" in output_context
