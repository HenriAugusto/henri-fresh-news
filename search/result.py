from RPA.Browser.Selenium import Selenium
from selenium.webdriver.remote.webelement import WebElement
from urllib.parse import urlparse
import os
import re
import requests

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
        self.__process_image()
        self.__check_if_contains_monetary_values()
        self.__count_search_phrases_in_title_and_description()

    def __scrap_title(self):
        title_element = self.browser.find_element("xpath:.//h4", self.element)
        self.title = title_element.text

    def __scrap_date(self):
        date_element = self.browser.find_element("xpath:.//span[@data-testid='todays-date']", self.element)
        self.date = date_element.text

    def __scrap_description(self):
        description_query = self.browser.find_elements("xpath:.//h4/../p", self.element)
        if description_query:
            description_element = self.browser.find_element(description_query[0], self.element)
            self.description = description_element.text
        else:
            self.description = None
            print("Result does NOT have description")

    def __process_image(self):
        img_element_query = self.browser.find_elements("xpath:.//figure//img", self.element)
        if img_element_query:
            self.img_url = img_element_query[0].get_attribute("src")
            a = urlparse(self.img_url)
            self.img_file_name = os.path.basename(a.path)
            self.__download_image()
        else:
            self.img_url = None
            self.img_file_name = None
            print("Result does NOT have an image")

    def __download_image(self):
        response = requests.get(self.img_url, stream=True)
        response.raise_for_status()
        self.img_path = os.path.join(Result.img_download_dir, self.img_file_name)
        with open(self.img_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"image successfully downloaded at {self.img_path}")

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
        print(f"title: {self.title}")
        print(f"date: {self.date}")
        print(f"description: {self.description}")
        print(f"img url: {self.img_url}")
        print(f"img file name: {self.img_file_name}")
        print(f"contains monetary values: {self.contains_monetary_values}")
        print(f"# of search phrases in result: {self.search_phrases_in_title_and_description}")