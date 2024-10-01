import time
import random
from typing import Optional, Dict
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import cloudscraper
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask
from loguru import logger

class SecurityBypass:
    def __init__(self, anticaptcha_key: Optional[str] = None):
        self.ua = UserAgent()
        self.anticaptcha_key = anticaptcha_key
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
        )
    
    def get_random_user_agent(self) -> str:
        return self.ua.random
    
    def get_with_cloudscraper(self, url: str) -> str:
        try:
            response = self.scraper.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Cloudscraper failed: {str(e)}")
            return None

    def get_with_selenium(self, url: str) -> str:
        options = uc.ChromeOptions()
        options.add_argument(f'--user-agent={self.get_random_user_agent()}')
        options.add_argument('--headless')
        
        driver = uc.Chrome(options=options)
        try:
            driver.get(url)
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            return driver.page_source
        except TimeoutException:
            logger.error("Selenium timeout waiting for page load")
            return None
        finally:
            driver.quit()

    def solve_captcha(self, url: str, site_key: str) -> Optional[str]:
        if not self.anticaptcha_key:
            logger.warning("No anticaptcha key provided")
            return None
        
        try:
            client = AnticaptchaClient(self.anticaptcha_key)
            task = NoCaptchaTaskProxylessTask(url, site_key)
            job = client.createTask(task)
            job.join(maximum_time=60)
            return job.get_solution_response()
        except Exception as e:
            logger.error(f"Captcha solving failed: {str(e)}")
            return None

class RequestManager:
    def __init__(self, anticaptcha_key: Optional[str] = None):
        self.security = SecurityBypass(anticaptcha_key)
        self.delays = [1, 2, 3, 5, 8]  # Fibonacci sequence for delays
    
    def _delay(self):
        delay = random.choice(self.delays)
        time.sleep(delay)

    def get_page_content(self, url: str, max_retries: int = 3) -> Optional[str]:
        methods = [
            ('cloudscraper', self.security.get_with_cloudscraper),
            ('selenium', self.security.get_with_selenium)
        ]
        
        for attempt in range(max_retries):
            for method_name, method in methods:
                try:
                    logger.info(f"Attempting to fetch {url} with {method_name}, attempt {attempt + 1}")
                    content = method(url)
                    if content:
                        return content
                except Exception as e:
                    logger.error(f"{method_name} attempt failed: {str(e)}")
                
                self._delay()
        
        logger.error(f"All attempts to fetch {url} failed")
        return None
