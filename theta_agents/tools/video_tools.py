import logging
from gradio_client import Client as client_gradio
from theta_agents.config.default_config import global_config

logger = logging.getLogger(__name__)

def create_video_from_image(filename_or_url: str) -> str:
    """
    Create a video from an image (URL or filename) and return the video URL.
    """
    try:
        config = global_config["capabilities"]["image_tools"]["create_video_from_image"]
        edgecloud_endpoint = config["edgecloud_endpoint"]
        edgecloud_endpoint_type = config["edgecloud_endpoint_type"]

        if edgecloud_endpoint_type == "gradio":
            client = client_gradio(edgecloud_endpoint)
            result = client.predict(
                filename_or_url,
                api_name="/predict"
            )
            return result.get('url', '')
        else:
            logger.error("Invalid edgecloud endpoint type.")
            return "Error: Invalid endpoint type."
    except Exception as e:
        logger.error(f"Failed to create video: {e}")
        return "Error: Failed to create video."