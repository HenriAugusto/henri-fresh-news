from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.keys import Keys
from search.result import Result
from data.data import DataManager
import re
from datetime import datetime
from logger.logger import Log

class Search:
    """ Responsible for all interactions with the NYTimes
        website related to searching phrases and it's related activities
        such as setting section filters, loading more search results, etc
    """

    search_form_status_locator = "xpath://p[@data-testid='SearchForm-status']"

    def __init__(
            self,
            search_phrase: str,
            sections: list[str],
            months: int,
            browser: Selenium,
            data_manager: DataManager):
        self.search_phrase = search_phrase
        self.sections = sections
        self.months = months
        self.browser = browser
        self.data_manager = data_manager

    def search(self) -> None:
        """ Searches for the search phrase. No other filters are applied """

        Log.info(f"searching for {self.search_phrase}")
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
        self.__wait_for_results_to_load()
        self.__get_total_number_of_results()
        Log.info(f"Number of results found {self.total_results}")

    def select_sections(self) -> None:
        """ Perform filtering for the desired sections.

            For simplicity, sections that are not found are ignored.
        """
        Log.info(f"Selecting sections {self.sections}")
        if self.sections.count:
            self.browser.click_element("xpath://*[@data-testid='search-multiselect-button']")
            for s in self.sections:
                section_selector = f"xpath://text()[normalize-space()='{s}']/../../input"
                if self.browser.does_page_contain_element(section_selector):
                    self.browser.click_element(section_selector)
                    Log.info(f"Requested section {s} was found and selected.")
                else:
                    Log.info(f"Requested section {s} was NOT found. Ignoring...")
        self.__wait_for_results_to_load()

    def set_search_range(self) -> None:
        """ Set the date filter on the website """
        start_date, end_date = self.__get_search_range_datetimes()
        Log.info(f"Setting search range: {start_date}-{end_date}")
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

    def process_results(self):
        result_last_index = 0

        while self.__show_more():
            results = self.__get_results()
            for i in range(result_last_index, len(results)):
                Log.info(f"\n\n---PARSING NEWS RESULT: {i}")
                r = results[i]
                try:
                    result = Result(self.browser, r, self.search_phrase)
                    Log.info(result)
                    if not self.data_manager.check_if_result_was_already_processed(result):
                        self.data_manager.write_result(result)
                        result.download_image()
                    else:
                        Log.info(f"Result {result.title} was already processed")
                except Exception as ex:
                    Log.info(f"Error caught while scraping result: {ex}")
                result_last_index += 1

        Log.info("finished processing all results for transaction")

    def __get_search_range_datetimes(self):
        """ Gets both the start and end date according to be used with the search """
        end_date = date.today()
        months_to_subtract = max(1, self.months) # index is 1-based and 0 is to be treated as 1
        delta = relativedelta(months=months_to_subtract-1)
        start_date = end_date-delta
        start_date = start_date.replace(day=1)
        return start_date, end_date

    def __show_more(self) -> bool:
        """ Tries to click the "Shows more" button.

            Returns true if it there were more results to load.
        """
        show_more_btn_locator = "xpath://button[@data-testid='search-show-more-button']"
        show_more_btn_query = self.browser.find_elements(show_more_btn_locator)
        if show_more_btn_query:
            results_before = len(self.__get_results())
            self.browser.click_button(show_more_btn_locator)
            # we tried a more "selenium-ish" implementation but as of now
            # wait_until_page_does_not_contain_element() is not working properly
            # with the limit argument
            # self.browser.wait_until_page_does_not_contain_element(
            #     show_more_btn_locator,
            #     timeout = timedelta(seconds=1000),
            #     limit=results_before
            # )
            max_wait_time = timedelta(seconds=20)
            start_time = datetime.now()
            while len(self.__get_results()) == results_before:
                if datetime.now()-start_time > max_wait_time:
                    raise TimeoutError("Timeout while waiting more results to load after clicking 'Show more'")
        return bool(show_more_btn_query)

    def __get_results(self):
        results_locator = "xpath://ol[@data-testid='search-results']/li[@data-testid='search-bodega-result']"
        return self.browser.find_elements(results_locator)

    def __wait_for_results_to_load(self):
        """ Wait news results to load after typing into the search bar and submitting

            NOT intended to use when clicking "Show more"
        """
        # When results are loading, there is an element that displays "Loading"
        # You might have to throttle your web browser to see this happening.
        # We first try to detect the "Loading" message, but we ignore if it
        # wasn't found because the results may load before the check,
        # (the "Loading" message already appeared and disappeared.)
        # In that case waitingfor the element to NOT contain "Loading" will work
        try:
            self.browser.wait_until_element_contains(
                Search.search_form_status_locator,
                "Loading",
                timeout=timedelta(seconds=10)
            )
        except Exception as ex:
            pass
        self.browser.wait_until_element_does_not_contain(
            Search.search_form_status_locator,
            "Loading"
        )

    def __get_total_number_of_results(self):
        search_status_text: str = self.browser.get_text(Search.search_form_status_locator)
        number_match = re.search("(\d|\,|\.)+", search_status_text)
        # In our experience, the website might show the thousands separator as
        # an comma or period, depending on the browser, so we remove both before parsing
        if number_match:
            match_str = number_match.group().replace(",", "").replace(".", "")
            self.total_results = int(match_str)
        else:
            raise Exception(
                f"Error while getting total number of results. Could not get value from string: {search_status_text}"
            )