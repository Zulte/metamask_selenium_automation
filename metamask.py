from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from loguru import logger

class Metamask:
    def __init__(self, driver):
        """
        Initialize with the Selenium WebDriver instance.
        """
        try:
            self.driver = driver
            logger.info("Metamask initialized with driver.")
        except Exception as e:
            logger.exception("Error initializing Metamask")
            pass
    
    def _click_element(self, element):
        self.driver.find_element(By.XPATH, f'{element}').click()
        
    
    def login_to_metamask(self, recovery_words):
        """
        Logs into MetaMask by navigating through the onboarding flow, entering the recovery phrase words and setting a password.
        """
        try:
            self._click_element('/html/body/div[1]/div/div[2]/div/div/div/ul/li[1]/div/input')
            self._click_element('/html/body/div[1]/div/div[2]/div/div/div/ul/li[3]/button')
            self._click_element('/html/body/div[1]/div/div[2]/div/div/div/div[2]/button[1]')
            for index, word in enumerate(recovery_words):
                input_id = f"import-srp__srp-word-{index}"
                try:
                    input_element = self.driver.find_element(By.ID, input_id)
                    input_element.clear()
                    input_element.send_keys(word)
                    #logger.info(f"Entered recovery word {index + 1}.")
                except Exception as e:
                    logger.exception(f"Error entering word {index + 1}: {e}")
                    self.driver.save_screenshot(f"screenshot_error_word_{index + 1}.png")
                    break
            self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[4]/div/button").click()
            password = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input")
            password1 = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input")
            password.send_keys('qwerty123456')
            password1.send_keys('qwerty123456')
            self._click_element("/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[3]/label/span[1]/input")
            self._click_element("/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/button")
            time.sleep(1)
            try:
                self._click_element("/html/body/div[1]/div/div[2]/div/div/div/div[3]/button")
            except Exception:
                self._click_element("//button[normalize-space(text())='Done']")
            self._click_element("/html/body/div[1]/div/div[2]/div/div/div/div[2]/button")
            self._click_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/button")
            logger.info("Logged into MetaMask successfully.")
        except Exception as e:
            logger.exception("Error in login_to_metamask")
            self.driver.save_screenshot('metamask_login.png')
            pass

    def register_new_wallet(self):
        """
        Registers a new MetaMask wallet by guiding through the setup process and retrieving the generated recovery phrase.
        
        return: list of recovery words
        """
        try:
            wait = WebDriverWait(self.driver, 10)
            self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#onboarding/welcome')
            time.sleep(3)
            self.driver.switch_to.window(self.driver.window_handles[0])
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/ul/li[1]/div/input'))).click()
            self._click_element('/html/body/div[1]/div/div[2]/div/div/div/ul/li[2]/button')
            self._click_element('/html/body/div[1]/div/div[2]/div/div/div/div[2]/button[1]')
            password = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input")
            password1 = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input")
            password.send_keys('qwerty123456')
            password1.send_keys('qwerty123456')
            self._click_element('/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[3]/label/span[1]/input')
            self._click_element('/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/button')
            wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/button[2]"))).click()
            self._click_element("/html/body/div[1]/div/div[2]/div/div/div/div[6]/button")
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[5]/div')))
            chips = self.driver.find_elements(By.CSS_SELECTOR, "div[data-testid^='recovery-phrase-chip-']")
            recovery_words = [chip.text for chip in chips]
            logger.info(f"New wallet registered with recovery phrase: {recovery_words}")
            return recovery_words
        except Exception as e:
            logger.exception("Error in register_new_wallet")
            pass

    def approve_connect(self):
        """
        Iterates through all open browser windows, prints each window's title,
        and when it finds the window with a title containing 'notification.html',
        it focuses on that window and executes JavaScript to click the confirmation button.
        After that, it checks if the target window is still open. If it is,
        the function is re-invoked.
        """
        javascript = """
            var buttons = document.getElementsByTagName('button');
            for (var i = 0; i < buttons.length; i++) {
                if (buttons[i].getAttribute('data-testid') === 'confirmation-submit-button' || 
                    buttons[i].getAttribute('data-testid') === 'confirm-btn' || 
                    buttons[i].getAttribute('data-testid') === 'confirm-footer-button') {
                    buttons[i].click();
                    break;
                }
            }
            """
        try:
            time.sleep(2)
            #logger.info(f"Number of window handles: {len(self.driver.window_handles)}")
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#onboarding/home')
            time.sleep(2)
            self.driver.refresh()
            time.sleep(5)
            self.driver.execute_script(javascript)
            time.sleep(2)
            logger.info("approve_connect completed.")
        except Exception as e:
            logger.exception("Error in approve_connect")
            pass

    def switch_network(self):
        """
        Switches the MetaMask network by navigating to network settings, entering the password,
        and triggering the network change via JavaScript.
        """
        javascript = """
        var buttons = document.getElementsByTagName('p');
        for (var i = 0; i < buttons.length; i++) {
            if (buttons[i].textContent == 'Linea') {
                buttons[i].click();
                break;
            }
        }"""
        try:
            wait = WebDriverWait(self.driver, 10)
            self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#')
            input("Press Enter after any manual steps if needed...")  # Blocking input if necessary
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/form/div/div/input'))).send_keys('qwerty123456')
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/button'))).click()
            time.sleep(3)
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[1]/button'))).click()
            self.driver.execute_script(javascript)
            logger.info("Network switched successfully.")
        except Exception as e:
            logger.exception("Error in switch_network")
            pass

    def connect(self):
        """
        Executes JavaScript to click a confirmation button across open browser windows for approval actions.
        """
        javascript = """
        var buttons = document.getElementsByTagName('button');
        for (var i = 0; i < buttons.length; i++) {
            if (buttons[i].getAttribute('data-testid') === 'confirm-btn') {
                buttons[i].click();
                break;
            }
        }
        """
        try:
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#onboarding/home')
            time.sleep(2)
            self.driver.refresh()
            time.sleep(5)
            self.driver.execute_script(javascript)
            time.sleep(2)
            logger.info("connect completed successfully.")
        except Exception as e:
            logger.exception("Error in connect")
            pass

    def sign_in(self):
        """
        Executes JavaScript to click a confirmation button across open browser windows for approval actions.
        """
        javascript = """
            var buttons = document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {
                if (buttons[i].textContent.trim() === 'Confirm'){
                    buttons[i].click();
                    break;
                }
            }
        """
        try:
            self.driver.switch_to.window(self.driver.window_handles[1])
            time.sleep(2)
            self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#onboarding/home')
            time.sleep(2)
            self.driver.refresh()
            time.sleep(5)
            self.driver.execute_script(javascript)
            time.sleep(2)
            logger.info("sign_in completed successfully.")
        except Exception as e:
            logger.exception("Error in sign_in")
            pass



    def pass_or_login(self, wallet):
      try:
        time.sleep(1)
        self.driver.switch_to.new_window('tab')
        self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#onboarding/welcome')
        time.sleep(10)
        try:
          self.driver.find_element(By.XPATH, '//*[@id="password"]')
          logger.info('Password send')
          self.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('qwerty123456')
          time.sleep(2)
          self.driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/button').click()
          time.sleep(2)
          return True
        except Exception:
          pass
        try:
          if self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/ul/li[1]/div/input'):
              self.login_to_metamask(wallet)
              return True
        except Exception:
          pass
      except Exception as e:
        print('Oops....')
        self.driver.save_screenshot('ooops.png')
        

if __name__ == "__main__":
    metamask = Metamask()
    metamask.register_new_wallet()
    pass