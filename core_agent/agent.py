"""Core agent implementation using Pydantic AI."""

import asyncio

# from typing import Union
from dotenv import load_dotenv
from dataclasses import dataclass

from rich.live import Live
from rich.text import Text
from rich.syntax import Syntax
from rich.markdown import CodeBlock, Markdown
from rich.console import Console, ConsoleOptions, RenderResult

from pydantic_ai import Agent
# from pydantic import BaseModel
# from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool

from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter


from prompts import MAIN_SYSTEM_PROMPT

load_dotenv()


# Dependency class
@dataclass
class CoreAgentDeps:
    """
    Dependencies required by the agent.
    """

    vector_store: InMemoryVectorStore


# # Response class
# class CodeDetails(BaseModel):
#     """
#     Structured response returned by the agent.
#     """

#     message: str  # Main message of the response
#     agent_py_content: str | None = None  # Content related to agent.py
#     tools_py_content: str | None = None  # Content related to tools.py
#     prompts_py_content: str | None = None  # Content related to prompts.py
#     env_example_content: str | None = None  # Content related to .env.example
#     requirements_txt_content: str | None = None  # Content related to requirements.txt


# class NoCodeGenerated(BaseModel):
#     """
#     Invalid response class for handling errors.
#     """


# CoreAgentResponse = Union[CodeDetails, NoCodeGenerated]

# Initialize the agent
core_agent = Agent(
    model="openai:gpt-4o", system_prompt=MAIN_SYSTEM_PROMPT, deps_type=CoreAgentDeps
)


def load_in_memory_vector_store() -> InMemoryVectorStore:
    """
    Load the in-memory vector store.
    """
    print("Loading vector store...")
    vector_store = InMemoryVectorStore(
        embedding=OllamaEmbeddings(model="mxbai-embed-large")
    )
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    pydantic_ai_doc = TextLoader("pydantic-ai-doc.txt", encoding="utf-8")
    pydantic_ai_docs = text_splitter.split_documents(pydantic_ai_doc.load())

    vector_store.add_documents(
        documents=pydantic_ai_docs,
    )

    return vector_store


def prettier_code_blocks():
    """Make rich code blocks prettier and easier to copy.

    From https://github.com/samuelcolvin/aicli/blob/v0.8.0/samuelcolvin_aicli.py#L22
    """

    class SimpleCodeBlock(CodeBlock):
        def __rich_console__(
            self, console: Console, options: ConsoleOptions
        ) -> RenderResult:
            code = str(self.text).rstrip()
            yield Text(self.lexer_name, style="dim")
            yield Syntax(
                code,
                self.lexer_name,
                theme=self.theme,
                background_color="default",
                word_wrap=True,
            )
            yield Text(f"/{self.lexer_name}", style="dim")

    Markdown.elements["fence"] = SimpleCodeBlock


async def run_agent():
    """
    Run the agent asynchronously.
    """

    prettier_code_blocks()

    deps = CoreAgentDeps(vector_store=load_in_memory_vector_store())
    console = Console()
    prompt = "How can I create a weather agent?"
    console.log(f"Asking: {prompt}...", style="cyan")
    with Live("", console=console, vertical_overflow="visible") as live:
        async with core_agent.run_stream(prompt, deps=deps) as result:
            async for message in result.stream():
                live.update(Markdown(message))
                console.log(message)
    console.log(result.usage())


# Example usage
if __name__ == "__main__":
    asyncio.run(run_agent())
