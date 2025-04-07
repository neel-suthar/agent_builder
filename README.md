# Agent Builder

Agent Builder is a framework for creating AI agents using Pydantic AI. It provides a structured approach to building fully functional agents by leveraging the power of Pydantic AI's type-safe and model-agnostic design.

## Features

- **Model-Agnostic**: Supports multiple LLM providers like OpenAI, Anthropic, Gemini, and more.
- **Type-Safe**: Ensures robust type checking for all components.
- **Extensible**: Easily add custom tools, prompts, and agents.
- **Python-Centric**: Designed with Python developers in mind.

## Installation

To get started, clone the repository and install the dependencies:

```bash
git clone https://github.com/your-username/agent-builder.git
cd agent-builder
uv install
```

## Usage

### Example: Creating a Custom Agent

1. **Define the Agent**: Create an agent in `agent.py` using Pydantic AI's `Agent` class.
2. **Add Tools**: Define tools in `tools.py` that the agent can use.
3. **Set Prompts**: Customize prompts in `prompts.py` to guide the agent's behavior.

#### Example Code

**agent.py**
```python
from pydantic_ai import Agent

agent = Agent(
    model="openai:gpt-4",
    system_prompt="You are a helpful assistant.",
)
```

**tools.py**
```python
from pydantic_ai.tools import Tool

class CalculatorTool(Tool):
    async def run(self, input: str) -> str:
        return str(eval(input))
```

**prompts.py**
```python
MAIN_SYSTEM_PROMPT = """
You are an expert assistant. Answer questions concisely and accurately.
"""
```

### Running the Agent

```bash
python core_agent/agent.py
```

## Environment Variables

Set up the required environment variables in a `.env` file or use the provided `.env.example`:

```
OPENAI_API_KEY=your_api_key_here
```

## Contributing

We welcome contributions! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and add tests if applicable.
4. Submit a pull request with a detailed description.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

For questions or support, join the `#pydantic-ai` channel in the [Pydantic Slack](https://logfire.pydantic.dev/docs/join-slack/) or open an issue on GitHub.

## Acknowledgments

This project is built on top of [Pydantic AI](https://github.com/pydantic/pydantic-ai). Special thanks to the Pydantic team for their amazing work!
