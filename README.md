
# Theta Agents SDK

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

The **Theta Agents SDK** is a Python library designed to help developers quickly build AI agent frameworks on the Theta EdgeCloud network. The SDK provides a range of prebuilt capabilities based on EdgeCloud's off-the-shelf containers, such as generating images and videos (Stable Diffusion), using EdgeCloud-hosted LLMs for underlying agent reasoning (e.g. Llama, Mistral) and writing code (CodeLlama), and Theta-specific capabilities like deploying to EdgeStore and the Theta Video API.

![alt](https://i.imgur.com/bBgAOYZ.png)

## Features

- **Create Images from Prompts**: Use EdgeCloud-hosted (or custom containers on EdgeCloud) image models like Stable Diffusion.
- **Create Videos from Images**: Generate videos using Stable Diffusion (Video) from EdgeCloud.
- **Generate Smart Contracts**: Easily create smart contracts based on user-defined prompts through CodeLlama hosted on EdgeCloud.
- **Deploy Smart Contracts**: Use web3-based agent tools to deploy to the Theta Testnet.
- **Upload files to Theta network's services**: Agents can upload files to EdgeCloud and videos to Theta's video services network.
- _**Coming soon:**_ Support for multi-agent workflows (2+ agents collaborating autonomously to solve tasks).

## Installation

To install the Theta Agents SDK, clone the repository and install the dependencies:

```bash
git clone https://github.com/yourusername/theta-agents-sdk.git
cd theta-agents-sdk

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .
```

## Setup

### 1. Environment Variables

Create a `.env` file in the root directory of your project. This file should contain all sensitive information such as API keys and private keys. Here's an example `.env` and you can look at `.env.example` for more:

```ini
# .env

HUGGING_FACE_TOKEN=your-hugging-face-token
GRADIO_API_KEY=your-gradio-api-key
BLOCKCHAIN_PRIVATE_KEY=your-blockchain-private-key # if deploying to Theta's chain.
```

### 2. Configuration File

Copy `config_template.yaml` to `config.yaml` and edit the values to match your specific setup:

```bash
cp config_template.yaml config.yaml
```

Edit `config.yaml` to include your specific configuration details, such as endpoints, model names, and environment variable names.

```yaml
llm_endpoint: "https://gemma2b....onthetaedgecloud.com/v1/chat/completions"
llm_model_name: "google/gemma-2b"

capabilities:
  image_tools:
    create_image_from_prompt:
      edgecloud_endpoint: "https://stablediffi...onthetaedgecloud.com"
      edgecloud_endpoint_type: "gradio"
  video_tools:
    create_video_from_image:
      edgecloud_endpoint: "https://stablediffi...onthetaedgecloud.com"
      edgecloud_endpoint_type: "gradio"
  smart_contract_tools:
    generate_smart_contract:
      edgecloud_endpoint: "..."
      edgecloud_endpoint_type: "openai"
      model_name: "..."
```

## Usage

### Running the Chat Interface

To interact with an AI agent using the terminal chat interface, you can use the following code snippet in your script:

```python
from theta_agents import ThetaAgent, create_image_from_prompt, create_video_from_image

# Load environment variables
load_dotenv()

# Initialize the agent
agent = ThetaAgent(
    capabilities=[create_image_from_prompt, create_video_from_image],
    show_planning=True,
    persona="You are a social media marketing expert."
)

def chat(agent: ThetaAgent):
    """
    Function to interact with the ThetaAgent in a chat-like interface in the terminal.
    """
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Exiting the chat.")
            break

        # Get the response from the agent
        response_data = agent(user_input)

        # Extract and display the user-facing message and internal planning message
        human_facing_text = response_data.get('user_facing_text', '')  # The text meant for the user
        planning_text = response_data.get('planning_text', '')  # Internal planning details
        error_message = response_data.get('error', '')  # Any error messages

        if human_facing_text:
            print(f"\033[96mAI:\033[0m {human_facing_text}")  # Cyan text for AI messages
        if planning_text:
            print(f"\033[93mInternal Plan:\033[0m {planning_text}")  # Yellow text for internal planning messages
        if error_message:
            print(f"\033[91mError:\033[0m {error_message}")  # Red text for errors

# Start the chat
chat(agent)
```

### Additional Capabilities

To add more capabilities (tools), update the `config.yaml` with the new tool configurations and ensure that the necessary environment variables are set.

## Contributing

We welcome contributions! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch-name`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch-name`).
5. Open a pull request.

Please ensure that your code adheres to our coding standards and passes all tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to the open-source community for providing the tools and libraries that make this project possible.
