import slack
import os
from pathlib import Path
from dotenv import load_dotenv
import ssl
import sys
import certifi

DATASET_DIR = '/Users/logancheng/Downloads/RESULTS' #'/data2/pypi'
PREVIOUS_NUMBER_OF_FILES = '/home/lsc210003/numfiles.txt'
def saved_previous_count(file_path: Path) -> int:
    if not os.path.exists(file_path):
        return 0
    with open(file_path) as f:
        contents = f.read()
        return int(contents) if contents.isdecimal() else 0
def count_files(dataset_dir: Path) -> int:
    return len(os.listdir(dataset_dir))
def save_file_count(file_path: Path, file_count: int):
    with open(file_path, 'w') as f:
        f.write(str(file_count))
def send_slack_message(text: str):
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    client = slack.WebClient(token=os.environ['SLACK_TOKEN'], sel = ssl_context)
    client.chat_postMessage(channel='#pypi-dataset-daily', text=text)

def main():
    existing_files = saved_previous_count(PREVIOUS_NUMBER_OF_FILES)
    current_files = count_files(DATASET_DIR)
    delta = current_files - existing_files

    message = f'Today, {delta} new files were downloaded. The PyPI dataset now has {current_files} files'
    send_slack_message(message)

    save_file_count(PREVIOUS_NUMBER_OF_FILES, current_files)
if __name__ == '__main__':
        main()
