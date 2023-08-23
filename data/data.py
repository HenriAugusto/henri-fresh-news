import csv
from search.result import Result

class DataManager:
    """ Encapsulates logic related to persitence of data.

        Contains methods to read and write results to the disk and check
        which result was already written.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.__load_results()

    def __load_results(self):
        self.results = []
        with open(self.file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                self.results.append(row)
        print("results loaded")

    def write_result(self, result: Result):
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.__result_to_row(result))

    def __result_to_row(self, result: Result):
            return [
                result.title,
                result.date,
                result.description,
                result.img_url,
                result.img_file_name,
                result.contains_monetary_values,
                result.search_phrases_in_title_and_description
            ]

    def check_if_result_was_already_processed(self, result):
        for r in self.results:
            title = r[0]
            date = r[1]
            if title == result.title and date == result.date:
                return True
        return False