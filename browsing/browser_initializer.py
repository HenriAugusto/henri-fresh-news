from RPA.Browser.Selenium import Selenium
from logger.logger import Log

class BrowserInitializer:
    """ Contains methods to initialize the browser state needed for processing transactions

        It opens the browser on the desired website and gets rid of any popup or dialog
        that might block interacting with the search bar.
    """
    NYTIMES_URL = "www.nytimes.com"
    compliance_overlay_continue_btn_locator = "//div[@id='complianceOverlay']//button"
    accept_cookies_btn_locator = "//button[@data-testid='GDPR-accept']"

    def __init__(self, browser: Selenium):
        self.browser = browser

    def initialize_browser(self) -> None:
        """ Opens the browser and leaves it in the state needed for processing transactions """
        self.browser.open_browser(self.NYTIMES_URL)
        self.browser.set_selenium_implicit_wait(5)
        self.browser.maximize_browser_window()

        # The robot might find an pop up+overlay asking to accept the changes in the ToS
        compliance_btn = self.browser.find_element(self.compliance_overlay_continue_btn_locator)
        if compliance_btn:
            self.browser.click_element(compliance_btn)

        # The "do you want some cookies, sweetheart?" stuff should
        # always appear but we check it just in case
        if self.browser.does_page_contain_element(self.accept_cookies_btn_locator):
            self.browser.click_element(self.accept_cookies_btn_locator)
            Log.info("accepting cookies")
        else:
            Log.info("no need to accept cookies")

    def kill_browser(self) -> None:
        """ Closes the browser """
        self.browser.close_all_browsers()