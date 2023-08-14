# Libraries
from robocorp.tasks import task
from robocorp import workitems
from RPA.Browser.Selenium import Selenium
# Our classes
from search.search import Search
from browsing.browser_initializer import BrowserInitializer

@task
def scrap_fresh_news():
    browser = Selenium()
    browser_initializer = BrowserInitializer(browser)
    browser_initializer.initialize_browser()

    for item in workitems.inputs:
        try:
            print("Processing Work Item")
            print(item.payload)
            search_phrase = item.payload['search_phrase']
            sections = item.payload['sections']
            months = item.payload['months']
            search = Search(search_phrase, sections, months, browser)
            search.search()
            search.select_sections()
        except Exception as ex:
            print(f"Error caught while processing transaction: {ex}")
            browser_initializer.kill_browser()
            browser_initializer.initialize_browser()

    print("End process")


if __name__ == "__main__":
    scrap_fresh_news()