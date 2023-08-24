import csv
import os
from datetime import datetime
from search.result import Result

class DataManager:
    """ Encapsulates logic related to persitence of data.

        Contains methods to read and write extracted news data to the disk and check
        which ones were already written.

        For simplicity we write an CSV file instead of an xlsx.
    """

    def __init__(self, file_path: str):
        """ Initializes the DataManager with a given file to store/retrieve data """
        self.file_path = file_path
        self.__load_results()

    def write_result(self, result: Result) -> None:
        """ Writes a single row (Result) to the file """
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.__result_to_row(result))

    def check_if_result_was_already_processed(self, result) -> bool:
        """ Returns if the result was already found in the CSV file """
        # There's room for optimizing this method's performance, but let's keep it
        # simple for the challenge
        for r in self.results:
            title = r[0]
            date = datetime.strptime(r[1], '%Y-%m-%d')
            if title == result.title and date == result.date:
                return True
        return False

    def __result_to_row(self, result: Result):
            return [
                result.title,
                result.date.strftime('%Y-%m-%d'),
                result.description,
                result.img_url,
                result.img_file_name,
                result.contains_monetary_values,
                result.search_phrases_in_title_and_description
            ]

    def __load_results(self):
        self.results = []
        if os.path.exists(self.file_path):
            with open(self.file_path, newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter=",", quotechar="\"")
                for row in reader:
                    self.results.append(row)
            print(f"results loaded from file {self.file_path}")
        else:
            print(f"file {self.file_path} was not found while loading results.")