import logging
from gradio_client import Client as client_gradio
from openai import OpenAI
from theta_agents.config.default_config import global_config

logger = logging.getLogger(__name__)

def create_image_from_prompt(prompt: str) -> str:
    """
    Create an image based on a prompt and return the image URL.
    """
    try:
        config = global_config["capabilities"]["image_tools"]["create_image_from_prompt"]
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
            return result.get('url', '')

        elif edgecloud_endpoint_type == 'openai':
            client = OpenAI(api_key=api_key, base_url=edgecloud_endpoint)
            response = client.images.generate(
                model=model_name,
                prompt=prompt,
                size="256x256",
                n=1
            )
            image_url = response.data[0].url
            return image_url

        else:
            logger.error("Invalid edgecloud endpoint type.")
            return "Error: Invalid endpoint type."

    except Exception as e:
        logger.error(f"Failed to create image: {e}")
        return "Error: Failed to create image."
