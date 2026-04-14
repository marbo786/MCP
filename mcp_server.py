from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(

    name = "read document content",
    description = "Read the contents of the document and return it as a string to" # this is basically a prompt to claude

)

def read_document(

    doc_id: str = Field(description="ID of the document to read")
):
    
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    
    return docs[doc_id]




@mcp.tool(
    name = "edit document",
    description = "Edit a document by replacing a string in the documents content with whatever user says"
)

def edit_document(

    doc_id: str = Field(description="ID of the document that will be edited"),
    old_str: str = Field(description="the text to replace"),
    new_str: str = Field(description="the new text to insert in place of the old text")
):
    
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    
    docs[doc_id] = docs[doc_id].replace(old_str,new_str)



@mcp.resource(
    name="list documents",
    description="Return a list of all available document IDs"
)
def list_documents():
    return list(docs.keys())



@mcp.resource(
    name="get document",
    description="Return the contents of a specific document"
)
def get_document(
    doc_id: str = Field(description="ID of the document to retrieve")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    
    return docs[doc_id]


@mcp.prompt(
    name="rewrite as markdown",
    description="Rewrite the given document into clean markdown format"
)
def rewrite_as_markdown(
    content: str = Field(description="Original document content")
):
    return f"""
You are a helpful assistant.

Rewrite the following document into well-structured Markdown format.
- Use headings where appropriate
- Use bullet points if needed
- Keep the meaning unchanged

Document:
{content}
"""

@mcp.prompt(
    name="summarize document",
    description="Summarize the given document concisely"
)
def summarize_document(
    content: str = Field(description="Document content to summarize")
):
    return f"""
You are a helpful assistant.

Summarize the following document in a concise way.
- Focus on key points
- Keep it short but informative

Document:
{content}
"""


if __name__ == "__main__":
    mcp.run(transport="stdio")
