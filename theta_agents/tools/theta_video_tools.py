import logging
import requests
from theta_agents.config.default_config import global_config

logger = logging.getLogger(__name__)

def _get_presigned_url_and_upload_id(filepath, service_account_id, service_account_secret):
      
      url = 'https://api.thetavideoapi.com/upload'
      headers = { 'x-tva-sa-id': service_account_id, 'x-tva-sa-secret': service_account_secret }

      response = requests.post(url, headers=headers)
      response_data = response.json()

      if response.status_code == 200 and response_data['status'] == 'success':
          upload_info = response_data['body']['uploads'][0]
          pre_signed_url = upload_info['presigned_url']
          upload_id = upload_info['id']
          return pre_signed_url, upload_id
      return None, None   

def _upload_video(filepath, pre_signed_url):
    with open(filepath, 'rb') as file:
        response = requests.put(pre_signed_url, headers={'Content-Type': 'application/octet-stream'}, data=file)
    return response.status_code == 200

def _transcode_video(upload_id, service_account_id, service_account_secret):
    url = 'https://api.thetavideoapi.com/video'
    headers = {
        'x-tva-sa-id': service_account_id,
        'x-tva-sa-secret': service_account_secret,
        'Content-Type': 'application/json'
    }
    data = {
        "source_upload_id": upload_id,
        "playback_policy": "public",
        "nft_collection": "0x5d0004fe2e0ec6d002678c7fa01026cabde9e793",
        "metadata": {
            "key": "value"
        }
    }
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    if response.status_code == 200 and response_data['status'] == 'success':
        video_id = response_data['body']['video_id']
    else:
        return None
    
def _get_video_playback_url(video_id, service_account_id, service_account_secret):
    url = f'https://api.thetavideoapi.com/video/{video_id}'
    headers = {
        'x-tva-sa-id': service_account_id,
        'x-tva-sa-secret': service_account_secret
    }

    response = requests.get(url, headers=headers)
    response_data = response.json()

    if response.status_code == 200 and response_data['status'] == 'success':
        video_info = response_data['body']['videos'][0]
        playback_uri = video_info.get('playback_uri')
        if playback_uri:
            return playback_uri
        else:
            return None
    else:
        return None    

def upload_video_to_theta(filepath: str) -> str:
    """
    Uploads a viddo to Theta's Video Delivery Network.
    """
    try:
      config = global_config["capabilities"]["theta_video_tools"]["upload_video_to_theta"]
      service_account_id = config["service_account_id"]
      service_account_secret = config["service_account_secret"]

      pre_signed_url, upload_id = _get_presigned_url_and_upload_id(filepath, service_account_id, service_account_secret)

      if pre_signed_url is None:
          return "Error: Failed to get pre-signed URL."
      if upload_id is None:
          return "Error: Failed to get upload ID."
      
      is_video_upload_successful = _upload_video(filepath, pre_signed_url)

      if not is_video_upload_successful:
          return "Error: Failed to upload video." 
      
      video_id = _transcode_video(upload_id, service_account_id, service_account_secret)
      if video_id is None:
          return "Error: Failed to transcode video."
      
      playback_uri = _get_video_playback_url(video_id, service_account_id, service_account_secret)
      if playback_uri is None:
          return "Error: Failed to get playback URI."
      else:
          return playback_uri

    except Exception as e:
        logger.error(f"Failed to upload video: {e}")
        return "Error: " + str(e)