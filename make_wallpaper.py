from wallpaper import get_wallpaper, set_wallpaper
from PIL import Image, ImageDraw, ImageFont
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import schedule
import time
import os
import logging


 
from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%d/%B/%Y, %H:%M:%S")
with open('Yayy.txt','w') as f:
    f.write(dt_string)

basic_paper = "windows.PNG"
windows10 = Image.open(basic_paper)
corona_img_path = "screenshot.png"
vaccine_img_path = "vac_screenshot.png"
def save_corona_screenshot(driver, target_url, img_path, button=True):
    driver.get(target_url)
    if button:
        close_buttons = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#root-portal > div > button')))
        time.sleep(2)
        visible_buttons = [close_button for close_button in close_buttons if close_button.is_displayed()]
        visible_buttons_len = len(visible_buttons)

        for i in range(visible_buttons_len):
            print(str(i) + "try")
            try:
                visible_buttons[visible_buttons_len - 1 - i].click()
            except Exception as e:
                print(e)
                pass
    
    time.sleep(2)
    if not 'error' in driver.page_source:
        driver.save_screenshot(img_path)

def crop_img(img_path):
    corona_screen = Image.open(img_path)
    width, height = corona_screen.size

    area = (width // 3 + 150, 0, width // 3 * 2 + 150, height)
    cropped = corona_screen.crop(area)
    return cropped

def make_wallpaper():
    cropped_corona = crop_img(corona_img_path)
    if os.path.exists(vaccine_img_path):
        vaccine_corona = crop_img(vaccine_img_path)
        area_one = (1920 // 3, 0)


    area_two = (1920 // 3 * 2, 0)
    windows10.paste(cropped_corona, area_two)
    if os.path.exists(vaccine_img_path):
        windows10.paste(vaccine_corona, area_one)
 
    # get a font
    fnt = ImageFont.truetype("BlackHanSans-Regular.ttf", 32)
    # get a drawing context
    draw = ImageDraw.Draw(windows10)
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S")
    draw.text((900,30), "마지막 업데이트 - " + dt_string, font=fnt, fill=(0,0,0))


    windows10.save(r'new_wallpaper.png')
    set_wallpaper(r'new_wallpaper.png')


def job():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("--no-startup-window")
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        save_corona_screenshot(driver, "https://corona-live.com/", img_path=corona_img_path)
        save_corona_screenshot(driver, "https://corona-live.com/vaccine", img_path=vaccine_img_path, button=False)
        driver.quit()
    except Exception as e:
        with open("anotherlog.txt", "a+") as f:
            error = str(e)
            print(error)
            f.write(error)
    make_wallpaper()

logging.basicConfig(filename="log.txt",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.info("Running corona wallpaper")

schedule.every(10).minutes.do(job)
job()
while True:
    schedule.run_pending()
    time.sleep(1)