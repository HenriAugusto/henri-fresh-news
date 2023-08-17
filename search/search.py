from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.keys import Keys

class Search:
    """ Responsible for all interactions with the NYTimes
        website related to searching phrases and it's related activities
        such as setting section filters, loading more search results, etc
    """

    def __init__(self, search_phrase: str, sections: list[str], months: int, browser: Selenium):
        self.search_phrase = search_phrase
        self.sections = sections
        self.months = months
        self.browser = browser

    def search(self):
        """ Searches for the search phrase. No other filters are applied """

        print(f"searching for {self.search_phrase}")
        # if it's our first search, we have to click the search button in the land page
        # and only then type into the input element.
        # Otherwise we have a different input to type into which is always visible.
        search_btn_locator = "xpath://button[@data-testid='search-button']"
        if self.browser.does_page_contain_element(search_btn_locator):
            self.browser.click_element(search_btn_locator)
            self.browser.input_text("xpath://*[@id='search-input']//input[@name='query']", self.search_phrase)
        else:
            self.browser.input_text("xpath://*[@id='searchTextField']", self.search_phrase)

        self.browser.click_element("xpath://button[@data-test-id='search-submit']")

    def select_sections(self):
        """ Perform filtering for the desired sections.

            For simplicity, sections that are not found are ignored.
        """

        print(f"Selecting sections {self.sections}")
        if self.sections.count:
            self.browser.click_element("xpath://*[@data-testid='search-multiselect-button']")
            for s in self.sections:
                section_selector = f"xpath://text()[normalize-space()='{s}']/../../input"
                if self.browser.does_page_contain_element(section_selector):
                    self.browser.click_element(section_selector)
                    print(f"Requested section {s} was found.")
                else:
                    print(f"Requested section {s} was NOT found. Ignoring...")

    def set_search_range(self):
        """ Set the date filter on the website """
        start_date, end_date = self.__get_search_range_datetimes()
        print(f"Start date: {start_date}")
        print(f"End date: {end_date}")
        # when inputing the dates as text in the <input> and pressing enter
        # the dates are considered as exlusive.
        # For ex: if you type the range 02/01/2023 - 10/01/2023
        # the website will consider the range 01/01/2023 - 09/01/2023.
        # For that reason we add one day to each date
        start_date = start_date + timedelta(days=1)
        end_date = end_date + timedelta(days=1)

        self.browser.click_element("xpath://button[@data-testid='search-date-dropdown-a']")
        self.browser.click_element("xpath://button[@aria-label='Specific Dates']")
        self.browser.input_text("id:startDate", start_date.strftime('%m/%d/%Y'))
        self.browser.input_text("id:endDate", end_date.strftime('%m/%d/%Y'))
        self.browser.press_keys(None, Keys.ENTER)

    def __get_search_range_datetimes(self):
        """ Gets both the start and end date according to be used with the search """
        end_date = date.today()
        months_to_subtract = max(1, self.months) # index is 1-based and 0 is to be treated as 1
        delta = relativedelta(months=months_to_subtract-1)
        start_date = end_date-delta
        start_date = start_date.replace(day=1)
        return start_date, end_date