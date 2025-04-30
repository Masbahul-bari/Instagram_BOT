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

def initialize_webdriver():
    option = Options()
    # option.add_argument("--headless")
    option.add_experimental_option("detach", False)
    driver = webdriver.Chrome(options=option)
    driver.implicitly_wait(1)
    # driver = webdriver.Chrome()
    driver.maximize_window()
    url = "https://www.instagram.com/"
    driver.get(url)
    return driver

def loging(driver):
    try:
        time.sleep(5)
        load_cookies(driver)
        time.sleep(5)
        # not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @tabindex='0' and text()='Not now']"))).click()
    except Exception as err:
        print(f"Error during loading cookies: {err}")        
        username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

        username.clear()
        password.clear()

        username.send_keys("wallahwalli07")
        password.send_keys("Email@12!@#")

        log_in = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        log_in.click()
        not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @tabindex='0' and text()='Not now']")))
        not_now.click()
        time.sleep(5)
        save_cookies(driver)

def load_post_link(driver, post_links):
    for post_link in post_links:
        driver.execute_script(f"window.location.href = '{post_link}'")
        time.sleep(5)

        source = source_name(driver)

        trimmed_post_link = post_link.replace("https://www.instagram.com", "")
        new_post_link = f"https://www.instagram.com/{source}{trimmed_post_link}"
        driver.execute_script(f"window.location.href = '{new_post_link}'")

        url_screenshot = post_screenshot(driver, new_post_link)
        description_text = description(driver)
        posted_at = get_post_time(driver)
        like_count = like(driver)
        comments = comment(driver,new_post_link)
        number_of_comments = num_of_comment(comments)
        current_time = scrap_at()

        post_data = create_post_data(
            source, url_screenshot, post_link, description_text, posted_at, comments, like_count, number_of_comments, current_time
        )

        save_post_data(post_data, post_link)

def post_screenshot(driver, post_link):
    # driver.get_screenshot_as_file(f"/home/mesba/Documents/new/ss/{post_link}.png")
    try:
        image_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//div[@class='_aagu _aato']//img[@class='x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3'])[1]")))
        post_media_url = image_element.get_attribute("src")
        return post_media_url
    except:
        post_media_url = None
        return post_media_url
    # print("post link: ",post_link)
    # parsed_url = urlparse(post_link)
    # relative_path = parsed_url.path
    # print("media link: ",relative_path)
    
    # try:
    #     print("1")
    #     image_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//a[@href='{relative_path}']//img[@crossorigin='anonymous' and @style='object-fit: cover;']")))
    #     print("2")
    #     post_media_url = image_element.get_attribute("src")
    #     print("3")
    #     media_links = post_media_url
    #     print(media_links)
    #     return media_links
    # except:
    #     media_links = None
    #     print(media_links)
    #     return media_links

def description(driver):
    try:
        description_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='x5yr21d xw2csxc x1odjw0f x1n2onr6']//span[@class='x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj']")))
        description = description_element.text
        return description
    except:
        description = None
        return description

def get_post_time(driver):
    try:
        time_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//time[@class='x1p4m5qa']")))
        timestamp = time_element.get_attribute("datetime")
        
        formatted_date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")  
        posted_at = formatted_date.strftime("%Y-%m-%d %H:%M:%S")
        return posted_at
    except:
        posted_at = None
        return posted_at

def like(driver):
    try:
        like_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@role='link']/span[1]/span[1]")))
        like_text = like_element.text
        like_count = int("".join(filter(str.isdigit, like_text)))
        return like_count
    except:
        like_count = None
        return like_count

def comment(driver, new_post_link):
    comments = []
    # driver.execute_script(f"window.location.href = '{new_post_link}'")
    driver.implicitly_wait(2)
    while True:
        try:
            view_more_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@style='min-height: 40px;']//button[@class='_abl-']//div[@class='_abm0']"))
            )
            driver.execute_script("arguments[0].click();", view_more_button)
            time.sleep(2)  # Wait for comments to load
        except:
            break  # No more "View more comments" button

    # Locate all top-level comments
    time.sleep(3)
    comment_elements = driver.find_elements(By.XPATH, "//ul[@class='_a9ym']/div/li")
    for comment_element in comment_elements:
        try:
            # Extract comment details
            user_profile_picture = comment_element.find_element(By.XPATH, ".//img[@crossorigin='anonymous']").get_attribute("src")
            user_name = comment_element.find_element(By.XPATH, ".//span[@class='xt0psk2']//a[@role='link']").text
            user_profile_url = f"https://www.instagram.com/{user_name}/"
            comment_text = comment_element.find_element(By.XPATH, ".//div[@class='xt0psk2']").text
            comment_time = comment_element.find_element(By.XPATH, ".//time").get_attribute("datetime")
            formatted_date = datetime.strptime(comment_time, "%Y-%m-%dT%H:%M:%S.%fZ") 
            comment_time = formatted_date.strftime("%Y-%m-%d %H:%M:%S")

            # Extract replies for this comment
            comments_replies = []
            print(f"Scraping comment for {user_name}: {comment_text}")

            try:
                # **Find the "View Replies" button inside this comment only**
                reply_button = comment_element.find_element(By.XPATH, ".//ul[@class='_a9yo']//button[contains(., 'View replies')]")
                driver.execute_script("arguments[0].click();", reply_button)
                print(f"Clicked 'View Replies' for {user_name}")

                # **Wait for replies to load**
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//ul[@class='_a9yo']/div[@role='button']"))
                )
                time.sleep(2)  


                # click_reply = driver.find_element(By.XPATH, "//ul[@class='_a9ym']/li//ul[@class='_a9yo']//button[contains(., 'View replies')]")
                # click_reply.click()
                # time.sleep(5)  # Just to ensure replies are fully visible

                # **Now scrape the replies**
                reply_elements = comment_element.find_elements(By.XPATH, ".//ul[@class='_a9yo']/div[@role='button']")
                print(len(reply_elements))
                for reply_element in reply_elements:
                    try:
                        reply_user_profile_picture = reply_element.find_element(By.XPATH, ".//img[@crossorigin='anonymous']").get_attribute("src")
                        reply_user_name = reply_element.find_element(By.XPATH, ".//span[@class='xt0psk2']//a[@role='link']").text
                        reply_user_profile_url = f"https://www.instagram.com/{reply_user_name}/"
                        reply_comment_text = reply_element.find_element(By.XPATH, ".//div[@class='xt0psk2']").text
                        reply_comment_time = reply_element.find_element(By.XPATH, ".//time").get_attribute("datetime")
                        # Format the timestamp if needed
                        formatted_date = datetime.strptime(reply_comment_time, "%Y-%m-%dT%H:%M:%S.%fZ")  # Adjust format if necessary
                        reply_comment_time = formatted_date.strftime("%Y-%m-%d %H:%M:%S")

                        comments_replies.append({
                            "user_pro_pic": reply_user_profile_picture,
                            "comment_time": reply_comment_time,
                            "user_name": reply_user_name,
                            "user_profile_url": reply_user_profile_url,
                            "comment_text": reply_comment_text
                        })
                    except:
                        continue  # Skip if there's an issue with a specific reply
            except Exception as e:
                print(f"Error scraping replies for {user_name}: {e}")
                # print(f"No replies found for {user_name}")  # Debugging message

            # Append main comment & replies
            comments.append({
                "user_profile_picture": user_profile_picture,
                "comment_time": comment_time,
                "user_name": user_name,
                "user_profile_url": user_profile_url,
                "comment_text": comment_text,
                "comments_replies": comments_replies
            })
            print("1:",len(comments))
        except Exception as e:
            print(e)
            continue  # Skip if there's an issue with a specific comment
    return comments

def num_of_comment(comments):
    try:
        number_of_comment = len(comments)
        return number_of_comment
    except:
        number_of_comment = None
        return number_of_comment

def scrap_at():
    try:
        current_time = datetime.now().isoformat()
        formatted_date = datetime.strptime(current_time, "%Y-%m-%dT%H:%M:%S.%f")
        current_time = formatted_date.strftime("%Y-%m-%d %H:%M:%S")
        return current_time
    except:
        current_time = None
        return current_time

def source_name(driver):
    try:
        source_name = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//span[contains(@class, '_ap3a')])[1]"))).text
        return source_name
    except:
        source_name = None
        return source_name

def create_post_data(source, url_screenshot, post_link, description, posted_at, comments, like_count, number_of_comments, current_time):
    return {
        "type": "Profile",
        "source": source,
        "post_url": post_link,
        "post_url_web": None,
        "url_screenshot": url_screenshot,
        "post_title": None,
        "post_text": description,
        "posted_at": posted_at,
        "post_topic": {
            "status": None,
            "topic": {"label": None},
        },
        "comments": comments,
        "reactions": {
            "Total": like_count,
            "Like": like_count,
            "Love": None,
            "Haha": None,
            "Wow": None,
            "Sad": None,
            "Angry": None,
            "Care": None,
            "All": like_count,
        },
        "featured_image": [],
        "total_comments": len(comments) if comments else 0,
        "percent_comments": None,
        "total_views": None,
        "total_shares": None,
        "source_img": None,
        "checksum": None,
        "vitality_score": None,
        "scraping_duration": None,
        "scraped_at": current_time,
        "device": None,
        "source_id": None,
    }

    
def save_post_data(post_data, post_link):
    sanitized_filename = re.sub(r"[^\w\-_. ]", "_", post_link)[:100]
    filename = f"{sanitized_filename}.json"

    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(post_data, json_file, ensure_ascii=False, indent=4)

    print(f"Data saved to '{filename}'")


if __name__ == "__main__":
    driver = initialize_webdriver()
    loging(driver)
    post_links = ["https://www.instagram.com/p/DInlzDqvXpl/"]
    load_post_link(driver, post_links)
