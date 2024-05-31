from selenium import webdriver
import pyscreenshot as ImageGrab
import time
import json
import pyautogui


chrome_options = webdriver.ChromeOptions()

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
im.save('main.png')
pyautogui.click(targetX, targetY)  
time.sleep(2)

driver.get(url+"/robots.txt")

im = ImageGrab.grab()
im.save('robots.png')

time.sleep(5)
driver.quit()