import logging
from gradio_client import Client as client_gradio
from openai import OpenAI
from theta_agents.config.default_config import global_config

logger = logging.getLogger(__name__)
logging.getLogger('httpx').setLevel(logging.ERROR)

def generate_smart_contract(prompt: str) -> str:
    """
    Generate smart contract code based on a user's prompt.
    """
    try:
        config = global_config["capabilities"]["smart_contract_tools"]["generate_smart_contract"]
        edgecloud_endpoint = config["edgecloud_endpoint"]
        edgecloud_endpoint_type = config["edgecloud_endpoint_type"]
        model_name = config["model_name"]
        api_key = config.get("api_key")

        if edgecloud_endpoint_type == "gradio":
            client = client_gradio(edgecloud_endpoint)
            result = client.predict(
                prompt,
                api_name="/predict"
            )
            return result.get('output', '')
        elif edgecloud_endpoint_type == 'openai':
            client = OpenAI(api_key=api_key, base_url=edgecloud_endpoint)
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content
            return content
        else:
            logger.error("Invalid edgecloud endpoint type.")
            return "Error: Invalid endpoint type."
    except Exception as e:
        logger.error(f"Failed to generate smart contract: {e}")
        return "Error: Failed to generate smart contract."