from seleniumwire import webdriver
import pyscreenshot as ImageGrab
import time
import json
import pyautogui


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')

with open('setting.json', 'r') as file:
        data = json.load(file)

driver = webdriver.Chrome(options=chrome_options)
x = data['robots']['x']
y = data['robots']['y']
driver.set_window_position(x,y)
driver.set_window_size(data['robots']['sizeX'], data['robots']['sizeY']) 

url = data['robots']['targetUrl']
driver.get(url)

time.sleep(2)
targetX = x + 150
targetY = y + 60
pyautogui.click(targetX, targetY)

time.sleep(1)
im = ImageGrab.grab()
im.save(f'./robot/{data["service_name"]}_main.png')
pyautogui.click(targetX, targetY)  
time.sleep(2)

# robots.txt URL로 이동
robots_url = url + "/robots.txt"
driver.get(robots_url)


time.sleep(2) 
request = None
for req in driver.requests:
    if req.response and req.url == robots_url:
        request = req
        break


if request:
    response_body = request.response.body.decode('utf-8')
    print("Response value of robots.txt:")
    print(response_body)
    
    robots_res_path = f'./robot/{data["service_name"]}_robots_res.txt'
    with open(robots_res_path, 'w', encoding='utf-8') as file:
        file.write(response_body)

else:
    print("Unable to find the request for robots.txt.")

im = ImageGrab.grab()
im.save(f'./robot/{data["service_name"]}_robots.png')

time.sleep(5)
driver.quit()