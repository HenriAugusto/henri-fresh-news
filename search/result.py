from RPA.Browser.Selenium import Selenium
from selenium.webdriver.remote.webelement import WebElement
from urllib.parse import urlparse
import os
import re
import requests
from datetime import datetime
from logger.logger import Log

class Result:
    """ Represents a single news result. Contains all the logic to extract and process the result data """

    img_download_dir = "output"

    def __init__(self, browser: Selenium, element: WebElement, search_phrase: str):
        """ The constructor conveniently does all the scraping at initialization """
        self.browser = browser
        self.element = element
        self.search_phrase = search_phrase
        self.__scrap_title()
        self.__scrap_date()
        self.__scrap_description()
        self.__scrap_image_url_and_name()
        self.__check_if_contains_monetary_values()
        self.__count_search_phrases_in_title_and_description()

    def download_image(self) -> bool:
        """ If the news have an image, downloads it.

            Returns if an image was downloaded
        """
        if self.img_url is not None:
            response = requests.get(self.img_url, stream=True)
            response.raise_for_status()
            self.img_path = os.path.join(Result.img_download_dir, self.img_file_name)
            with open(self.img_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            Log.info(f"image successfully downloaded at {self.img_path}")
        return self.img_url is not None

    def __scrap_title(self):
        title_element = self.browser.find_element("xpath:.//h4", self.element)
        self.title = title_element.text

    def __scrap_date(self):
        link_element = self.browser.find_element("xpath:.//a/h4/..", self.element)
        link_url = link_element.get_attribute("href")
        # real-world ex as reference:
        # www.nytimes.com/1951/09/02/archives/igor-stravinsky-conducts.html?searchResultPosition=6
        date_matches = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", link_url)
        y = int(date_matches.group(1))
        m = int(date_matches.group(2))
        d = int(date_matches.group(3))
        self.date = datetime(year=y, month=m, day=d)

    def __scrap_description(self):
        description_query = self.browser.find_elements("xpath:.//h4/../p", self.element)
        if description_query:
            description_element = self.browser.find_element(description_query[0], self.element)
            self.description = description_element.text
        else:
            self.description = None
            Log.info("Result does NOT have description")

    def __scrap_image_url_and_name(self):
        img_element_query = self.browser.find_elements("xpath:.//figure//img", self.element)
        if img_element_query:
            self.img_url = img_element_query[0].get_attribute("src")
            a = urlparse(self.img_url)
            self.img_file_name = os.path.basename(a.path)
        else:
            self.img_url = None
            self.img_file_name = None
            Log.info("Result does NOT have an image")

    def __check_if_contains_monetary_values(self):
        # Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD
        if self.description:
            numeric_base = "\d{1,3}(\,\d{1,3})*(\.\d{1,2})?"
            full_regex = f"(\${numeric_base})|({numeric_base} (dollars|USD))"
            self.contains_monetary_values = bool(re.search(full_regex, self.description))
        else:
            self.contains_monetary_values = None

    def __count_search_phrases_in_title_and_description(self):
        needle = self.search_phrase.lower()
        haystack = self.title.lower()
        if self.description:
            haystack += f" {self.description.lower()}"
        self.search_phrases_in_title_and_description = haystack.count(needle)

    def __str__(self):
        return (f"title: {self.title}\n"
                f"date: {self.date}\n"
                f"description: {self.description}\n"
                f"img url: {self.img_url}\n"
                f"img file name: {self.img_file_name}\n"
                f"contains monetary values: {self.contains_monetary_values}\n"
                f"# of search phrases in result: {self.search_phrases_in_title_and_description}")