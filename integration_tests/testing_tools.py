from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import sys

class SeleniumTestCase(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        service = Service(f"{settings.BASE_DIR}/chromedriver")
        # cls.driver = webdriver.Chrome(service=service, options=options)
        cls.driver = webdriver.Remote(
            f"http://localhost:4444/wd/hub", options=options
        )
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def tearDown(self):
        if sys.exc_info()[0]:
            test_method_name = self._testMethodName
            self.driver.save_screenshot("selenium-error-%s.png" % test_method_name)
        super().tearDown()

