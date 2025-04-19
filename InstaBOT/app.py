from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from datetime import datetime
import time
import re
import json
from urllib.parse import urlparse

import os
from cookies import load_cookies, save_cookies

# import wget

option = Options()
# option.add_argument("--headless")
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=option)
driver.implicitly_wait(1)

# driver = webdriver.Chrome()
driver.maximize_window()
url = "https://www.instagram.com/"
driver.get(url)

try:
    time.sleep(5)
    load_cookies(driver)
    time.sleep(5)
    # not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @tabindex='0' and text()='Not now']"))).click()
except:        
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    username.clear()
    password.clear()

    username.send_keys("wallahwalli07")
    password.send_keys("Email@12!@#")

    log_in = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @tabindex='0' and text()='Not now']"))).click()
    time.sleep(5)
    save_cookies(driver)




keyword = "Sunset"

keyword_URL = f"https://www.instagram.com/explore/search/keyword/?q=%23{keyword}"
driver.execute_script(f"window.location.href = '{keyword_URL}'")

a = input("Enter any key")

# Scroll and collect post links
post_links = set()
# post_media_url = []
previous_length = 0
scroll_attempts = 0
max_scroll_attempts = 1  # Stop scrolling after this many attempts with no new links

while scroll_attempts < max_scroll_attempts:
    # Get all post links on the current page
    links = driver.find_elements(By.XPATH, "//div[@class='x78zum5 xdt5ytf xwrv7xz x1n2onr6 xph46j xfcsdxf xsybdxg x1bzgcud']//a[@href]")
    for link in links:
        post_links.add(link.get_attribute("href"))
    
    # Scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3) 
    # Check if new links were added
    if len(post_links) > previous_length:
        previous_length = len(post_links)
        # scroll_attempts = 0  # Reset scroll attempts if new links are found
        scroll_attempts += 1
    else:
        # scroll_attempts += 1  # Increment attempts if no new links are found
        scroll_attempts = 0
        
# Print all post links
print(f"Total Posts Collected: {len(post_links)}")
for post_link in post_links:
    driver.execute_script(f"window.location.href = '{post_link}'")
    time.sleep(3)

    try:
        Source = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='xyinxu5 x1pi30zi x1g2khh7 x1swvt13']//span[@class='xjp7ctv']//span[@class='_ap3a _aaco _aacw _aacx _aad7 _aade']"))).text
        print(Source)
    except:
        print(Source)

    try:
        Post_Text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='x5yr21d xw2csxc x1odjw0f x1n2onr6']//span[@class='x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj']"))).text
        print(Post_Text)
    except:
        Post_Text = None
        print(None)
    try:
        time_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//time[@class='x1p4m5qa']")))
        timestamp = time_element.get_attribute("datetime")
        
        # Format time
        formatted_date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        posted_at = formatted_date.strftime("%Y-%m-%d %H:%M:%S")
        print(posted_at)
    except:
        posted_at = None
        print(posted_at)
    
    try:
        URL = post_link
        print(URL)
    except:
        URL = None
        print(URL)

    post_data = {
        "source": Source,
        "Post_Text": Post_Text,
        "Date": posted_at,
        "URL": URL
    }

    sanitized_filename = re.sub(r'[^\w\-_. ]', '_', post_link)[:100]
    filename = f"{sanitized_filename}.json"

    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(post_data, json_file, ensure_ascii=False, indent=4)

    print(f"Data saved to '{filename}'")

driver.quit()
