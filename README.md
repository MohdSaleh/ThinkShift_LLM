# tShift_LLM 🧠🔀

[![PyPI version](https://badge.fury.io/py/tshift-llm.svg)](https://badge.fury.io/py/tshift-llm)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/tshift-llm.svg)](https://pypi.org/project/tshift-llm/)

tShift_LLM is a robust and flexible LLM manager that seamlessly shifts between multiple language models to ensure uninterrupted AI-powered conversations. Say goodbye to API limitations and hello to consistent, reliable responses!

## 🌟 Key Features

- 🔄 **Automatic Failover**: Shifts between models when errors occur, ensuring you always get a response.
- 🔌 **Multi-Provider Support**: Works with various LLM providers (OpenAI, Anthropic, Cohere, etc.).
- 🌊 **Streaming & Non-Streaming**: Supports both streaming and non-streaming completions.
- 📊 **Detailed Logging**: Keeps track of all interactions for analysis and debugging.
- ⚖️ **Load Balancing**: Uses round-robin selection to distribute requests across clients.
- 🛡️ **Rate Limit Protection**: Helps bypass API limitations by switching to available clients.

## 🤔 Why tShift_LLM?

In the real world, LLM APIs often come with limitations:

- ⏱️ Requests per minute
- 🕰️ Requests per hour
- 📅 Requests per day

These constraints can be a roadblock for applications requiring consistent access to LLM capabilities. tShift_LLM solves this by managing multiple LLM clients automatically, ensuring you get a successful response even if some clients fail due to these limitations.

## 🚀 Quick Start

### Installation

```bash
pip install tshift-llm
```

```bash
# Latest release
pip install tshift-llm==0.2.2
```

### Basic Usage

```python
from tshift_llm import tShift_LLM, LiteLLMClient

# Set up your clients
clients = [
    LiteLLMClient(
        model="gpt-3.5-turbo", 
        api_key="your-openai-key-1",
        api_base="your-openai-url"
    ),
    LiteLLMClient("gpt-3.5-turbo", "your-openai-key-2"),
    LiteLLMClient("claude-2", "your-anthropic-key"),
    LiteLLMClient("command-nightly", "your-cohere-key")
]

# Initialize tShift_LLM
tshift_llm = tShift_LLM(clients)

# Make a completion request
response = tshift_llm.completion(
    messages=[{"role": "user", "content": "What's the meaning of life?"}]
)
print(response.choices[0].message.content)
```

## 🛠️ Advanced Usage

### Streaming Completions

```python
for chunk in tshift_llm.stream_completion(
    messages=[{"role": "user", "content": "Write a short story about AI."}]
):
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

### Custom Error Handling

```python
try:
    response = tshift_llm.completion(messages=[...])
except Exception as e:
    print(f"All LLM clients failed. Last error: {str(e)}")
```

## 📊 Logging

tShift_LLM automatically logs all interactions. You can find the log file at `tshift_llm.log` in your working directory.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [LiteLLM](https://github.com/BerriAI/litellm) for providing a unified interface to various LLM providers.
- All the amazing LLM providers out there pushing the boundaries of AI.

## 🌟 Star Us!

If you find tShift_LLM helpful, please consider giving us a star on GitHub. It helps us know that our work is valuable and encourages further development!

[![GitHub stars](https://img.shields.io/github/stars/MohdSaleh/tshift-llm.svg?style=social&label=Star)](https://github.com/MohdSaleh/tshift-llm)

---

Made with ❤️ by [Ryan Saleh]

Got questions? [Open an issue](https://github.com/MohdSaleh/tshift-llm/issues) or reach out to us at hello@ryansaleh.com