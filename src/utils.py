import os
import sys

import dill

from src.exception import CustomException
import json
import base64
from requests import get, post
from dotenv import load_dotenv

    
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)

# Working with Spotify
    
load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes),'utf-8')

    url = 'https://accounts.spotify.com/api/token' #post request url

    headers = { # post request headers
        "Authorization": "Basic "+ auth_base64,
        "Content-Type": "application/x-www-form-urlencoded" 
    } 

    data = {'grant_type': 'client_credentials'} #post request body

    result = post(url, headers=headers, data = data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def get_auth_header(token):
    return {'Authorization': 'Bearer ' + token}