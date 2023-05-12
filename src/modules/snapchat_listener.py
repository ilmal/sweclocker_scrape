import os
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

def get_element(driver, input, search_type="XPATH"):
    try:
        DELAY = 60
        if search_type == "XPATH":
            return WebDriverWait(driver, DELAY).until(EC.presence_of_element_located(
                (By.XPATH, str(input))))
        if search_type == "CLASS_NAME":
            return WebDriverWait(driver, DELAY).until(EC.visibility_of_all_elements_located(
                (By.CLASS_NAME, str(input))))
    except TimeoutException:
        print("Loading took too much time!")
        driver.quit()

def get_driver():

    print("sending snap")

    base_url = "https://web.snapchat.com/"

    dirname = os.path.dirname(__file__)
    driver_user_path = dirname.replace("modules", "driver_user")

    """
    
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36

    """

    options = webdriver.ChromeOptions()
    #options.add_argument("--window-size=1920,1080")
    #options.add_argument("--headless=new")
    #options.add_argument("--disable-gpu")
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    #options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
    options.add_argument(str('--user-data-dir=' + driver_user_path)) # use a custom profile


    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

    driver.get(base_url)

    return driver

def check_for_messages(driver):
    user_bodys = get_element(driver, "O4POs", "CLASS_NAME")

    print(user_bodys)

    for index, user_body in enumerate(user_bodys):
        name = user_body.find_element(By.XPATH, "./div[2]/span").text
        message = user_body.find_element(By.XPATH, "./div[2]/div").text

        if "New Chat" in message:
            print(name)
            return [name, user_bodys[index]]

def read_messages(driver, element):
    element.click()
    time.sleep(1)
    ActionChains(driver).send_keys(Keys.CONTROL + "R")
    time.sleep(1)

    chat_window = element.find_element(By.ID, "cv-415e9c75-260f-5452-b6e3-0d241ec92c22")
    
    print(chat_window.text)





def snap_listener():
    driver = get_driver()

    while True:
        new_messages = check_for_messages(driver)
        
        time.sleep(2)

        if new_messages:
            read_messages(driver, new_messages[1])


    
    

    time.sleep(1000)

    driver.quit()

if __name__ == "__main__":
    snap_listener()