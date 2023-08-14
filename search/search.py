from RPA.Browser.Selenium import Selenium

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