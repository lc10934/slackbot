import slack
import os
from pathlib import Path
from dotenv import load_dotenv
import ssl
import sys
import certifi

DATASET_DIR = '/data2/pypi'
PREVIOUS_NUMBER_OF_FILES = '/home/lsc210003/numfiles.txt'
try:
    with open(PREVIOUS_NUMBER_OF_FILES) as f:
        contents = f.readlines()
except FileNotFoundError:
    contents = 0
    print("file not found", file=sys.stderr)
list = os.listdir(DATASET_DIR) 
number_files = len(list)

if not contents:
    contents = 0

new_files = number_files - int(contents[0])

with open(PREVIOUS_NUMBER_OF_FILES, 'w') as f:
    f.write(str(number_files))
    
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

ssl_context = ssl.create_default_context(cafile=certifi.where())
client = slack.WebClient(token=os.environ['SLACK_TOKEN'], ssl=ssl_context)

client.chat_postMessage(channel='#test', text=new_files)
