import os
import requests
from bs4 import BeautifulSoup

def read_config(config_file):
    config = {}
    with open(config_file, 'r') as f:
        for line in f:
            if line.strip():
                key, value = line.strip().split('=')
                config[key.strip()] = value.strip()
    return config

def get_file_list(base_url):
    response = requests.get(base_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        file_links = soup.find_all('a')
        file_names = [link.get('href').split('/')[-1] for link in file_links if link.get('href')]
        return file_names
    else:
        print("Failed to retrieve file list.")
        return []

def download_file(base_url, local_directory, file_name):
    file_url = f"{base_url}{file_name}"
    local_file_path = os.path.join(local_directory, file_name)

    if not os.path.exists(local_directory):
        os.makedirs(local_directory)

    if os.path.exists(local_file_path):
        print(f"Skipping {file_name}, already exists.")
        return

    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        with open(local_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded {file_name}")
    else:
        print(f"Failed to download {file_name}")

def main():
    config = read_config('config.txt')
    if 'BASE_URL' in config and 'LOCAL_DIRECTORY' in config:
        base_url = config['BASE_URL']
        local_directory = config['LOCAL_DIRECTORY']
        files = get_file_list(base_url)
        for file in files:
            download_file(base_url, local_directory, file)
    else:
        print("BASE_URL or LOCAL_DIRECTORY not found in config file.")

if __name__ == "__main__":
    main()
