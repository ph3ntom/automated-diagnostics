import requests
import json
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

sys.setrecursionlimit(10**6)

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_links(url):
    """
    주어진 URL의 웹 페이지로부터 모든 링크를 추출하여 반환합니다.
    """
    links = set()
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # <a> 태그의 href 속성 추출
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            if is_valid_url(full_url):
                links.add(full_url)

        # <iframe> 태그의 src 속성 추출
        for iframe in soup.find_all('iframe', src=True):
            src = iframe['src']
            full_url = urljoin(url, src)
            if is_valid_url(full_url):
                links.add(full_url)

        # <img> 태그의 src 속성 추출
        for img in soup.find_all('img', src=True):
            src = img['src']
            full_url = urljoin(url, src)
            if is_valid_url(full_url):
                links.add(full_url)

        # <link> 태그의 href 속성 추출
        for link in soup.find_all('link', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            if is_valid_url(full_url):
                links.add(full_url)

        # <script> 태그의 src 속성 추출
        for script in soup.find_all('script', src=True):
            src = script['src']
            full_url = urljoin(url, src)
            if is_valid_url(full_url):
                links.add(full_url)

        # <form> 태그의 action 속성 추출
        for form in soup.find_all('form', action=True):
            action = form['action']
            full_url = urljoin(url, action)
            if is_valid_url(full_url):
                links.add(full_url)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
    
    return links

def passive_spider(start_url, depth=1):
    """
    주어진 URL에서 시작하여 Passive Spidering을 수행하고, 결과를 트리 구조로 txt 파일에 저장합니다.
    """
    visited_urls = set()
    urls_to_visit = {start_url}
    tree = {start_url: []}

    for _ in range(depth):
        new_urls = set()
        for url in urls_to_visit:
            if url not in visited_urls:
                print(f"Visiting: {url}")
                visited_urls.add(url)
                links = get_all_links(url)
                tree[url] = list(links)
                new_urls = new_urls.union(links)
        urls_to_visit = new_urls.difference(visited_urls)

    return tree

def save_tree_to_file(tree, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        queue = [(start_url, 0)]  # (URL, depth) 튜플로 구성된 큐
        while queue:
            url, depth = queue.pop(0)  # 큐의 첫 번째 항목을 가져옴
            indent = ' ' * depth  # 깊이에 따른 들여쓰기
            file.write(f"{indent}{url}\n")  # 파일에 URL과 들여쓰기 적용하여 쓰기
            # 현재 URL의 자식 URL들을 큐에 추가
            if url in tree:  # tree는 URL을 키로, 해당 URL의 자식 URL 리스트를 값으로 하는 딕셔너리라고 가정
                for child_url in tree[url]:
                    queue.append((child_url, depth + 4))  # 다음 깊이를 위해 4 증가

if __name__ == "__main__":
    # 시작 URL 및 Spidering 시작
    with open('setting.json', 'r') as file:
            data = json.load(file)

    start_url = data['url_parser']['startUrl']
    depth = data['url_parser']['depth']
    tree = passive_spider(start_url, depth)

    # 트리 구조를 txt 파일로 저장
    file_name = f"./urlParser/{data['service_name']}_spider_tree.txt"
    save_tree_to_file(tree, file_name)
