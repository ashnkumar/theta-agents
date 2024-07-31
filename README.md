
# Theta Agents SDK

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

The **Theta Agents SDK** is a Python library designed to help developers quickly build AI agent frameworks on the Theta EdgeCloud network. The SDK provides a range of prebuilt capabilities, such as generating images, creating videos, and developing smart contracts.

![alt](https://i.imgur.com/bBgAOYZ.png)

## Features

- **Create Images from Prompts**: Use models like OpenAI's DALL-E to generate images based on textual prompts.
- **Create Videos from Images**: Generate videos using specified models and endpoints.
- **Generate Smart Contracts**: Easily create smart contracts based on user-defined prompts.

## Installation

To install the Theta Agents SDK, clone the repository and install the dependencies:

```bash
git clone https://github.com/yourusername/theta-agents-sdk.git
cd theta-agents-sdk

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scriptsctivate`

# Install dependencies
pip install -e .
```

## Setup

### 1. Environment Variables

Create a `.env` file in the root directory of your project. This file should contain all sensitive information such as API keys and private keys. Here's an example `.env`:

```ini
# .env

OPENAI_API_KEY=your-openai-api-key
GRADIO_API_KEY=your-gradio-api-key
BLOCKCHAIN_PRIVATE_KEY=your-blockchain-private-key
```

### 2. Configuration File

Copy `config_template.yaml` to `config.yaml` and edit the values to match your specific setup:

```bash
cp config_template.yaml config.yaml
```

Edit `config.yaml` to include your specific configuration details, such as endpoints, model names, and environment variable names.

```yaml
llm_endpoint: "https://api.openai.com/v1"
llm_model_name: "gpt-4o-mini"

capabilities:
  image_tools:
    create_image_from_prompt:
      edgecloud_endpoint: "your-image-endpoint"
      edgecloud_endpoint_type: "openai"
      model_name: "dall-e-2"
      api_key_env: "OPENAI_API_KEY"
  video_tools:
    create_video_from_image:
      edgecloud_endpoint: "your-video-endpoint"
      edgecloud_endpoint_type: "gradio"
      model_name: "asdf"
      api_key_env: "GRADIO_API_KEY"
  smart_contract_tools:
    generate_smart_contract:
      edgecloud_endpoint: "your-smart-contract-endpoint"
      edgecloud_endpoint_type: "openai"
      model_name: "gpt-4o"
      api_key_env: "OPENAI_API_KEY"
      blockchain_private_key_env: "BLOCKCHAIN_PRIVATE_KEY"
```

## Usage

### Running the Chat Interface

To interact with an AI agent using the terminal chat interface, you can use the following code snippet in your script:

```python
from theta_agents import ThetaAgent, create_image_from_prompt, create_video_from_image, generate_smart_contract

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
