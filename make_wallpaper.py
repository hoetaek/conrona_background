from wallpaper import get_wallpaper, set_wallpaper
from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import schedule
import time
 
from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%d/%B/%Y, %H:%M:%S")
with open('Yayy.txt','w') as f:
    f.write(dt_string)

basic_paper = "windows.PNG"
windows10 = Image.open(basic_paper)
img_path = "screenshot.png"
def save_corona_screenshot():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("--no-startup-window")

    driver = webdriver.Chrome('chromedriver.exe', options=options)
    # driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://corona-live.com/')
    close_buttons = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#root-portal > div > button')))
    visible_buttons = [close_button for close_button in close_buttons if close_button.is_displayed()]
    visible_buttons_len = len(visible_buttons)

    for i in range(visible_buttons_len):
        visible_buttons[visible_buttons_len - 1 - i].click()
    

    driver.save_screenshot(img_path)
    driver.quit()


def make_wallpaper():
    corona_screen = Image.open(img_path)
    width, height = corona_screen.size

    area = (width // 3, 0, width // 3 * 2, height)
    cropped = corona_screen.crop(area)

    area = (1920 - width // 3, 0, 1920, height)
    windows10.paste(cropped, area)
    windows10.save('new_wallpaper.png')
    set_wallpaper('new_wallpaper.png')


def job():
    save_corona_screenshot()
    make_wallpaper()

schedule.every(10).minutes.do(job)
job()
while True:
    schedule.run_pending()
    time.sleep(1)