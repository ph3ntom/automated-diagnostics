import requests
from bs4 import BeautifulSoup
import json
import os
import hashlib

def is_login_successful(response):
    try:
        data = json.loads(response.text)
        if 'success' in data:
            return data['success']
    except json.JSONDecodeError:
        pass

    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find('script')
    if script_tag and 'location.href="/"' in script_tag.string:
        return True
    elif script_tag and 'location.href="index.asp?cmd=login"' in script_tag.string:
        return False
    else:
        return None

def save_request_response(login_url, data, headers, response, password):
    log_dir = "./limit_login_log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 비밀번호 해시 생성
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    filename = f"{log_dir}/{password_hash}.txt"

    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f'Request URL: {login_url}\n')
        f.write(f'Request Data: {str(data)}\n')
        f.write(f'Request Headers: {str(headers)}\n\n')
        f.write(f'Response Status Code: {response.status_code}\n')
        f.write(f'Response Text: {response.text}\n\n')

def login(username, password, login_url):
    response = requests.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    form = soup.find('form')
    method = form.get('method')
    action = form.get('action')

    data = {}
    for input_tag in form.find_all('input'):
        name = input_tag.get('name')
        value = input_tag.get('value')
        if input_tag.get('type') == 'hidden':
            data[name] = value
        elif name.lower() in ['id', 'email', 'username']:
            data[name] = username
        elif name.lower() in ['password', 'passwd', 'pwd']:
            data[name] = password

    if action.startswith('http://') or action.startswith('https://'):
        login_url = action
    else:
        login_url = f"{login_url}/{action}"

    headers = {'Content-Type': 'application/json'}
    response = requests.post(login_url, json=data, headers=headers)
    save_request_response(login_url, data, headers, response, password)

    if not is_login_successful(response):
        response = requests.post(login_url, data=data)
        save_request_response(login_url, data, {}, response, password)

    return response

def try_passwords(username, passwords, login_url):
    for password in passwords:
        print(f"비밀번호 시도: {password}")
        response = login(username, password, login_url)
        if is_login_successful(response) is True:
            print("로그인 성공!")
            return
        elif is_login_successful(response) is False:
            print("로그인 실패.")
        else:
            print("알 수 없는 응답")
    print("마지막 시도: 정확한 비밀번호")

if __name__ == "__main__":
    login_url = "http://192.168.60.131/member/index.asp"
    username = "phantom"
    wrong_passwords = ["dummy1", "dummy2", "dummy3", "dummy4", "dummy5", "dummy6", "dummy7"]
    correct_password = "1234"

    try_passwords(username, wrong_passwords, login_url)
    try_passwords(username, [correct_password], login_url)
