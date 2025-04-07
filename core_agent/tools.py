"""Tools used by the core agent."""

from typing import List

from pydantic_ai import RunContext
from langchain_core.documents import Document
from langchain_core.vectorstores.base import VectorStoreRetriever

from agent import core_agent
from agent import CoreAgentDeps


@core_agent.tool
async def search_pydantic_ai_docs(ctx: RunContext[CoreAgentDeps], query: str) -> str:
    """
    Retrieve the full Pydantic AI documentation.

    Args:
        query (str): The search query (not used in this implementation).

    Returns:
        str: The full content of the documentation file.
    """
    vector_store: VectorStoreRetriever = ctx.deps.vector_store.as_retriever()

    try:
        # Retrieve the document from the vector store
        docs: List[Document] = await vector_store.ainvoke(
            query=query,
        )
        # Extract the content from all the documents
        content = "\n".join([d.page_content for d in docs])

        return content
    except Exception as e:
        return f"Error retrieving documentation: {str(e)}"
