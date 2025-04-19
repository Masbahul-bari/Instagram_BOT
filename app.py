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

# username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
# password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

# username.clear()
# password.clear()

# username.send_keys("wallahwalli07")
# password.send_keys("Email@12!@#")

# log_in = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
# # not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @tabindex='0' and text()='Not now']"))).click()
# time.sleep(10)


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


# //div[@class="_aaqt"]//span[@class="xt0psk2"]


#Serarch box section:
# Search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='x1n2onr6']//span[text()='Search']"))).click()
# Search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='xjoudau x6s0dn4 x78zum5 xdt5ytf x1c4vz4f xs83m0k xrf2nzk x1n2onr6 xh8yej3 x1hq5gj4']//input[@placeholder='Search']")))
# Search_box.clear()
# Search_box.send_keys()




# not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
# click_search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Search')]")))
# click_search.click()
# searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
# searchbox.clear()

# keyword = "independent.television"
# # searchbox.send_keys(keyword)
# # searchbox.send_keys(Keys.ENTER)


# # first_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{keyword}') and @dir='auto']")))
# # f"//span[contains(text(), '{keyword}') and @dir='auto']"
# # driver.implicitly_wait(2)
# # first_option.click()
# driver.execute_script(f"window.location.href = '{url}{keyword}/'")
# time.sleep(5)
# # scrape the profile image
# try:
#     profile_img_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//section[contains(@class, 'x6s0dn4')]//a[@href='/{keyword}/']//img[@draggable='false']")))
#     profile_img_url = profile_img_element.get_attribute("src")
#     # print(f"Profile Image URL: {profile_img_url}")
# except Exception as e:
#     # print(f"Error scraping profile image: {e}")
#     profile_img_url = None


# # Scroll and collect post links
# post_links = set()
# # post_media_url = []
# previous_length = 0
# scroll_attempts = 0
# max_scroll_attempts = 2  # Stop scrolling after this many attempts with no new links

# while scroll_attempts < max_scroll_attempts:
#     # Get all post links on the current page
#     links = driver.find_elements(By.XPATH, "//div[@class='_ac7v x1f01sob xcghwft xat24cr xzboxd6']//a[@href]")
#     for link in links:
#         post_links.add(link.get_attribute("href"))
    
#     # Scroll down
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(3) 
#     # Check if new links were added
#     if len(post_links) > previous_length:
#         previous_length = len(post_links)
#         # scroll_attempts = 0  # Reset scroll attempts if new links are found
#         scroll_attempts += 1
#     else:
#         # scroll_attempts += 1  # Increment attempts if no new links are found
#         scroll_attempts = 0
# # Print all post links
# print(f"Total Posts Collected: {len(post_links)}")
# # for post_link in post_links:
# #     print(post_link)

# media_links={}
# for post_link in post_links:
#     # Scrape the post media (image or video thumbnail)
#     parsed_url = urlparse(post_link)
#     relative_path = parsed_url.path
    
#     try:
#         image_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//a[@href='{relative_path}']//img[@crossorigin='anonymous' and @style='object-fit: cover;']")))
#         post_media_url = image_element.get_attribute("src")
#         media_links[post_link] = post_media_url
#     except:
#         media_links[post_link] = None


# time.sleep(5)
# # Scrape descriptions for each post link
# for post_link in post_links:
#     try:
#         # Navigate to the post
#         driver.execute_script(f"window.location.href = '{post_link}'")
#         time.sleep(3)  # Wait for the page to load
        
#         # Scrape the description
#         try:
#             description_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='xt0psk2']/h1[@class='_ap3a _aaco _aacu _aacx _aad7 _aade']")))
#             description = description_element.text
#         except:
#             # If the description is not found, set it to None
#             description = None
        
#         # Try to scrape the post's timestamp
#         try:
#             time_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//time[@class='x1p4m5qa']")))
#             timestamp = time_element.get_attribute("datetime")
            
#             # Format the timestamp if needed
#             formatted_date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")  # Adjust format if necessary
#             posted_at = formatted_date.strftime("%Y-%m-%d %H:%M:%S")
#         except:
#             # If the timestamp is not found, set it to None
#             posted_at = None

#         # Scrape the like count
#         try:
#             like_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@role='link']/span[1]/span[1]")))
#             like_text = like_element.text
#             # Remove non-numeric characters for likes count
#             like_count = int("".join(filter(str.isdigit, like_text)))
#         except:
#             like_count = None  # If like count not found

#         # Scrape the post media (image or video thumbnail)
#         post_media_link = media_links[post_link]

#         # Scrap the comment
#         comments = []
#         while True:
#             try:
#                 view_more_button = WebDriverWait(driver, 2).until(
#                     EC.element_to_be_clickable((By.XPATH, "//div[@style='min-height: 40px;']//button[@class='_abl-']//div[@class='_abm0']"))
#                 )
#                 driver.execute_script("arguments[0].click();", view_more_button)
#                 time.sleep(2)  # Wait for comments to load
#             except:
#                 break  # No more "View more comments" button

#         # Locate all top-level comments
#         time.sleep(3)
#         comment_elements = driver.find_elements(By.XPATH, "//ul[@class='_a9ym']/div/li")

#         for comment_element in comment_elements:
#             try:
#                 # Extract comment details
#                 user_profile_picture = comment_element.find_element(By.XPATH, ".//img[@crossorigin='anonymous']").get_attribute("src")
#                 user_name = comment_element.find_element(By.XPATH, ".//span[@class='xt0psk2']//a[@role='link']").text
#                 user_profile_url = f"https://www.instagram.com/{user_name}/"
#                 comment_text = comment_element.find_element(By.XPATH, ".//div[@class='xt0psk2']").text
#                 comment_time = comment_element.find_element(By.XPATH, ".//time").get_attribute("datetime")
#                 formatted_date = datetime.strptime(comment_time, "%Y-%m-%dT%H:%M:%S.%fZ") 
#                 comment_time = formatted_date.strftime("%Y-%m-%d %H:%M:%S")

#                 # Extract replies for this comment
#                 comments_replies = []
#                 print(f"Scraping comment for {user_name}: {comment_text}")

#                 try:
#                     # **Find the "View Replies" button inside this comment only**
#                     reply_button = comment_element.find_element(By.XPATH, "//ul[@class='_a9ym']/li//ul[@class='_a9yo']//button[contains(., 'View replies')]")
#                     driver.execute_script("arguments[0].click();", reply_button)
#                     print(f"Clicked 'View Replies' for {user_name}")

#                     # **Wait for replies to load**
#                     WebDriverWait(driver, 5).until(
#                         EC.presence_of_element_located((By.XPATH, "//ul[@class='_a9yo']/div[@role='button']"))
#                     )
#                     time.sleep(2)  


#                     # click_reply = driver.find_element(By.XPATH, "//ul[@class='_a9ym']/li//ul[@class='_a9yo']//button[contains(., 'View replies')]")
#                     # click_reply.click()
#                     # time.sleep(5)  # Just to ensure replies are fully visible

#                     # **Now scrape the replies**
#                     reply_elements = comment_element.find_elements(By.XPATH, "//ul[@class='_a9yo']/div[@role='button']")
#                     print(len(reply_elements))
#                     for reply_element in reply_elements:
#                         try:
#                             reply_user_profile_picture = reply_element.find_element(By.XPATH, ".//img[@crossorigin='anonymous']").get_attribute("src")
#                             reply_user_name = reply_element.find_element(By.XPATH, ".//span[@class='xt0psk2']//a[@role='link']").text
#                             reply_user_profile_url = f"https://www.instagram.com/{reply_user_name}/"
#                             reply_comment_text = reply_element.find_element(By.XPATH, ".//div[@class='xt0psk2']").text
#                             reply_comment_time = reply_element.find_element(By.XPATH, ".//time").get_attribute("datetime")
#                             # Format the timestamp if needed
#                             formatted_date = datetime.strptime(reply_comment_time, "%Y-%m-%dT%H:%M:%S.%fZ")  # Adjust format if necessary
#                             reply_comment_time = formatted_date.strftime("%Y-%m-%d %H:%M:%S")

#                             comments_replies.append({
#                                 "user_pro_pic": reply_user_profile_picture,
#                                 "comment_time": reply_comment_time,
#                                 "user_name": reply_user_name,
#                                 "user_profile_url": reply_user_profile_url,
#                                 "comment_text": reply_comment_text
#                             })
#                         except:
#                             continue  # Skip if there's an issue with a specific reply
#                 except Exception as e:
#                     print(f"Error scraping replies for {user_name}: {e}")
#                     # print(f"No replies found for {user_name}")  # Debugging message

#                 # Append main comment & replies
#                 comments.append({
#                     "user_profile_picture": user_profile_picture,
#                     "comment_time": comment_time,
#                     "user_name": user_name,
#                     "user_profile_url": user_profile_url,
#                     "comment_text": comment_text,
#                     "comments_replies": comments_replies
#                 })
#             except:
#                 continue  # Skip if there's an issue with a specific comment
       
#         date_now = datetime.now().isoformat()
#         formatted_date = datetime.strptime(date_now, "%Y-%m-%dT%H:%M:%S.%f")  # Adjusted format
#         date_now = formatted_date.strftime("%Y-%m-%d %H:%M:%S")
#         try:
#             number_of_comment = len(comments)
#         except:
#             number_of_comment = None

#         # Prepare the post data
#         post_data = {
#             "type": "Profile",
#             "source": keyword,
#             "post_url": post_link,
#             "post_url_web": None,
#             "url_screenshot": post_media_link,
#             "post_title": None,
#             "posted_at": {
#                 "$date": posted_at
#             },
#             "post_text": description,
#             "post_topic": {
#                 "status": None,
#                 "topic": {
#                 "label": None
#                 }
#             },
#             "comments": comments,
#             "reactions": {
#                 "Total": like_count,
#                 "Sad": None,
#                 "Love": None,
#                 "Wow": None,
#                 "Like": like_count,
#                 "Haha": None,
#                 "Angry": None,
#                 "Care": None,
#                 "All": like_count
#             },
#             "featured_image": [],
#             "total_comments": number_of_comment,
#             "percent_comments": None,
#             "total_views": None,
#             "total_shares": None,
#             "source_img": profile_img_url,
#             "checksum": None,
#             "vitality_score": None,
#             "scraping_duration": None,
#             "scraped_at": {
#                 "$date": date_now
#             },
#             "device": None,
#             "source_id": None
#         }

#         # Create a safe filename using the post URL
#         sanitized_filename = re.sub(r'[^\w\-_. ]', '_', post_link)[:100]  # Truncate to 100 characters to avoid long filenames
#         filename = f"{sanitized_filename}.json"

#         # Save each post data to a separate JSON file
#         with open(filename, "w", encoding="utf-8") as json_file:
#             json.dump(post_data, json_file, ensure_ascii=False, indent=4)

#         print(f"Data saved to '{filename}'")

#     except Exception as e:
#         print(f"Error processing post {post_link}: {e}")

# print("Scraping completed.")

# driver.quit()
