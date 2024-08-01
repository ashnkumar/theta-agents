import logging
import time
import requests
from eth_account.messages import encode_defunct
from web3 import Web3
import json
from theta_agents.config.default_config import global_config

logger = logging.getLogger(__name__)

def upload_to_edgestore(filepath: str) -> str:
    """
    Uploads a file to the Edge Store network.
    """
    try:
        config = global_config["capabilities"]["theta_edgestore_tools"]["upload_to_edgestore"]
        w3_provider_endpoint = config["w3_provider_endpoint"]
        address = config["theta_wallet_public_address"]
        private_key = config["theta_wallet_private_key"]
        w3 = Web3(Web3.HTTPProvider(w3_provider_endpoint))

        # Step 1: Generate the authentication token
        timestamp = str(int(time.time() * 1000))
        message = f'Theta EdgeStore Call {timestamp}'
        message_encoded = encode_defunct(text=message)
        signed_message = w3.eth.account.sign_message(message_encoded, private_key=private_key)
        signature = signed_message.signature.hex()
        auth_token = f"{timestamp}.{address}.{signature}"

        # Step 2: Define the URL and headers for the request
        url = 'https://api.thetaedgestore.com/api/v2/data'
        headers = { 'x-theta-edgestore-auth': auth_token}

        # Step 3: Define the file to upload
        with open(filepath, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, headers=headers, files=files)

        # Step 4: Return response from Edge Store            
        try:
            response_json = response.json()
            return response_json
        except requests.exceptions.JSONDecodeError:
            return response.text    
    except Exception as e:
        logger.error(f"Failed to upload file: {e}")
        return "Error: " + str(e)