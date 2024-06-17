from tqdm import tqdm
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_url(url, path):
    full_url = f"{url}/{path}"
    try:
        response = requests.get(full_url)
        if response.status_code == 200:
            return f"Found: {full_url}\n"
        elif response.status_code == 403:
            return f"Forbidden: {full_url}\n"
    except requests.RequestException as e:
        return f"An error occurred: {e}\n"
    time.sleep(0.1)  # Introduce a delay of 0.1 seconds between requests
    return None

def dirBruteForce(url, wordlist, output_file):
    """
    주어진 URL에 대해 디렉토리 및 파일을 브루트 포스 방식으로 탐색하고 결과를 파일로 저장하는 함수
    """
    with open(wordlist, 'r') as file:
        paths = file.read().splitlines()
    
    with open(output_file, 'w') as out_file:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(fetch_url, url, path): path for path in paths}
            for future in tqdm(as_completed(futures), total=len(paths), desc="Processing paths"):
                result = future.result()
                if result:
                    out_file.write(result)

if __name__ == "__main__":
    url = "http://192.168.60.129"
    wordlist = "./wordlist/basic.txt"
    output_file = "./dirBruteForce/results.txt"
    dirBruteForce(url, wordlist, output_file)