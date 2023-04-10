from bs4 import BeautifulSoup as bs
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

URL="https://www.sweclockers.com/marknad/sok?searchid=f875f4bb-53d9-4121-ba5d-401ff1ff1fed"

def get_url():

    print("Getting url")

    base_url = "https://www.sweclockers.com/marknad"

    driver = webdriver.Chrome()

    driver.get(base_url)

    DELAY = 60

    def get_element(x_path):
        try:
            return WebDriverWait(driver, DELAY).until(EC.presence_of_element_located(
                (By.XPATH, str(x_path))))
        except TimeoutException:
            print("Loading took too much time!")
            driver.quit()


    # press cookie accept
    button = get_element(
        "/html/body/div[6]/div[2]/div/div[1]/div/div[2]/div/button[2]")
    button.click()

    # uncheck "Säljes"
    check_box = get_element(
        "/html/body/div[3]/div/div/div[4]/div[1]/div/div[1]/form/div[4]/div/div[4]/ul/li[1]")
    check_box.click()

    # uncheck "Köpes"
    check_box = get_element(
        "/html/body/div[3]/div/div/div[4]/div[1]/div/div[1]/form/div[4]/div/div[4]/ul/li[2]")
    check_box.click()

    # uncheck "Bytes"
    check_box = get_element(
        "/html/body/div[3]/div/div/div[4]/div[1]/div/div[1]/form/div[4]/div/div[4]/ul/li[3]")
    check_box.click()

    # select "Stockholm"
    select = get_element(
        "/html/body/div[3]/div/div/div[4]/div[1]/div/div[1]/form/div[4]/div/div[2]/div[1]/select")
    select = Select(select)
    select.select_by_visible_text("Stockholm")
    
    # press "sök"
    button = get_element(
        "/html/body/div[3]/div/div/div[4]/div[1]/div/div[1]/form/div[2]/button")
    button.click()

    url = driver.current_url

    driver.quit()

    return url





def handle_html(url):

    raw_html = requests.get(url).text

    soup = bs(raw_html, "html.parser")

    posts = soup.find("tbody", {"class": "body"})

    if not posts: print("No posts found!"); return False

    titles = [post.find("h2").text.replace("\n", "").replace("\t", "")[:-1] for post in posts.find_all("tr")]

    print(f"{str(len(posts))} posts found: {str(titles)}")

    return titles

def web_handler():

    url = get_url()

    titles = handle_html(url)