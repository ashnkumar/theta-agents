import logging
from gradio_client import Client as client_gradio
from web3 import Web3
from openai import OpenAI
from solcx import compile_source, install_solc
from theta_agents.config.default_config import global_config

install_solc('0.8.0')

logger = logging.getLogger(__name__)
logging.getLogger('httpx').setLevel(logging.ERROR)

def generate_smart_contract(prompt: str) -> str:
    """
    Generate smart contract code based on a user's prompt.
    """

    system_prompt = """
    Generate a smart contract for a decentralized voting application. The smart contract should include all relevant best practices and be as secure as possible. Return nothing but the smart contract code.
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
                    {"role": "system", "content": system_prompt},
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
    
def analyze_smart_contract(prompt: str) -> str:
    """
    Analyze smart contracts for security vulnerabilities, refactoring, etc.
    """

    system_prompt = """
    Analyze the smart contract for any security vulnerabilities, refactoring, or other issues. Return nothing but the analysis in the text form"""
    try:
        config = global_config["capabilities"]["smart_contract_tools"]["analyze_smart_contract"]
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
                    {"role": "system", "content": system_prompt},
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
    
def deploy_smart_contract(contract_source_code, 
                    contract_name, 
                    initial_supply=1000000):
    """
    Deploys a smart contract to the Theta testnet blockchain
    """
    
    config = global_config["capabilities"]["smart_contract_tools"]["deploy_smart_contract"]
    public_address = config["theta_wallet_public_address"]
    private_key = config["theta_wallet_private_key"]

    theta_rpc_url = "https://eth-rpc-api-testnet.thetatoken.org/rpc" #testnet
    w3 = Web3(Web3.HTTPProvider(theta_rpc_url))
    
    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol[f'<stdin>:{contract_name}']

    # Get the contract bytecode and ABI
    bytecode = contract_interface['bin']
    abi = contract_interface['abi']

    # Create the contract instance
    MyToken = w3.eth.contract(abi=abi, bytecode=bytecode)

    # Build the transaction
    nonce = w3.eth.get_transaction_count(public_address)
    tx = MyToken.constructor(initial_supply).build_transaction({
        'chainId': 365,  # Theta testnet chain ID
        'gas': 2000000,
        'gasPrice': 4000000000000,  # Minimum required gas price for Theta testnet
        'nonce': nonce,
    })

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_receipt.contractAddress