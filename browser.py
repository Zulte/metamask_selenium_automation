from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from metamask import Metamask
import time
from loguru import logger

# Configure logger to log errors to a file
logger.add("logs/errors.txt", level="ERROR", format="{time} {level} {message}")

class Browser:
    def __init__(self, driver_path="./drivers/chromedriver.exe", metamask_extension_path='./extensions/metamask.crx'):
        """
        Initializes the browser with the specified driver and Metamask extension.
        """
        chrome_options = Options()
        try:
            
            chrome_options.add_extension(metamask_extension_path)
            #chrome_options.add_argument("--headless=new")
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--disable-gpu")              
            chrome_options.add_argument("--disable-application-cache")
            chrome_options.add_argument("--disable-dev-shm-usage") 
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            chrome_options.add_argument("--window-size=1249,1225")
            
            self.driver = webdriver.Chrome(
                service=Service(executable_path=driver_path),
                options=chrome_options
            )
            
            self.metamask = Metamask(self.driver)
            logger.info("Browser initialized successfully.")
        except Exception as e:
            logger.exception("Error initializing Browser")
            raise

    def check_ip(self):
        try:
            self.driver.get('https://2ip.ua/ua/')
            time.sleep(5)
            try:
                self.driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/div[2]/div[2]/button[1]").click()
                #logger.info("Cookie banner clicked successfully.")
            except NoSuchElementException:
                logger.info("No cookie banner found.")
            ip = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div/div/div/div/article/section/div/div/div/div/div[2]").text
            logger.info(f"IP address: {ip}")
            user_agent = self.driver.execute_script("return navigator.userAgent;")
            logger.info(f"User agent: {user_agent}")
            return ip, user_agent
        except Exception as e:
            logger.exception("Error in check_ip method")
            pass
    
    
    def refresh_page(self):
        try:
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.refresh()
            logger.info("Page refreshed successfully.")
        except Exception as e:
            logger.exception("Error refreshing page")
            raise

    def quit(self):
        try:
            self.driver.close()
            self.driver.quit()
            logger.info("Browser quit successfully.")
        except Exception as e:
            logger.exception("Error quitting browser")
            raise

    