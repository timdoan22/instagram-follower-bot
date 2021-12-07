from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

INSTAGRAM_URL = "https://www.instagram.com/accounts/login/"
USER_NAME = USERNAME
PASSWORD = PASSWORD
FOLLOWER_ACCOUNT = "https://www.instagram.com/<USER_NAME>"
CHROME_DRIVER_PATH = YOUR_CHROME_DRIVER_PATH


class Instafollower:
    def __init__(self, driver_path):
        self.ser = Service(driver_path)
        self.options = Options()
        self.options.add_argument("user-data-dir=/tmp/tarun")
        self.driver = webdriver.Chrome(service=self.ser, options=self.options)

    def login(self):
        self.driver.get(INSTAGRAM_URL)
        self.driver.maximize_window()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "html")))

        try:
            self.driver.find_element(By.NAME, "username").send_keys(USER_NAME)
            self.driver.find_element(By.NAME, "password").send_keys(PASSWORD)
            self.driver.find_element(
                By.XPATH, '//*[@id="loginForm"]/div/div[3]/button').click()
        except Exception as error:
            pass

        try:
            self.driver.find_element(
                By.XPATH, '/html/body/div[5]/div/div/div/div[3]/button[2]').click()
        except Exception as error:
            pass

    def find_followers(self):
        self.driver.get(FOLLOWER_ACCOUNT)
        self.driver.maximize_window()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "html")))
        self.driver.find_element(
            By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]').click()

    def follow(self):
        scroll = 0
        pop_up_window = WebDriverWait(
            self.driver, 2).until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[6]/div/div/div[2]")))

        while scroll < 10:
            followers = self.driver.find_elements(By.CLASS_NAME, "sqdOP")
            for follower in followers:
                if follower.text == 'Follow':
                    follower.click()
                time.sleep(.5)

            self.driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                pop_up_window)
            scroll += 1

    def unfollow(self):
        scroll = 0
        pop_up_window = WebDriverWait(
            self.driver, 2).until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[6]/div/div/div[2]")))

        while scroll < 10:
            followers = self.driver.find_elements(By.CLASS_NAME, "sqdOP")
            for follower in followers:
                if follower.text != 'Follow':
                    follower.click()
                    try:
                        self.driver.find_element(
                            By.XPATH, "/html/body/div[7]/div/div/div/div[3]/button[1]").click()
                    except Exception as error:
                        pass

                    time.sleep(1)
                    try:
                        self.driver.find_element(
                            By.XPATH, "/html/body/div[7]/div/div/div/div[2]/button[2]").click()
                    except Exception as error:
                        pass
                time.sleep(.5)

            self.driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                pop_up_window)
            scroll += 1


ig_bot = Instafollower(CHROME_DRIVER_PATH)
ig_bot.login()
ig_bot.find_followers()
ig_bot.follow()
