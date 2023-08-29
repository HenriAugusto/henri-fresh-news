# Libraries
from robocorp.tasks import task
from robocorp import workitems
from RPA.Browser.Selenium import Selenium
# Our classes
from search.search import Search
from browsing.browser_initializer import BrowserInitializer
from data.data import DataManager
from logger.logger import Log

# Please read the README.md file regarding testing the robot

@task
def scrap_fresh_news():
    browser = Selenium()
    Log.initialize()
    browser_initializer = BrowserInitializer(browser)
    browser_initializer.initialize_browser()
    data_manager = DataManager("scrapped-news.csv")

    for item in workitems.inputs:
        try:
            Log.info(f"Processing Work Item:\n{item.payload}")

            search_phrase = item.payload['search_phrase']
            sections = item.payload['sections']
            months = item.payload['months']

            search = Search(search_phrase, sections, months, browser, data_manager)
            search.search()
            search.set_search_range()
            search.select_sections()
            search.process_results()

            Log.info("Transaction processed successfully")
        except Exception as ex:
            Log.error(f"Error caught while processing transaction: {ex}")
            browser_initializer.kill_browser()
            browser_initializer.initialize_browser()

    Log.info("End of the process")


if __name__ == "__main__":
    scrap_fresh_news()