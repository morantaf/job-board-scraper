import re
import csv
import time
from abc import ABC, abstractmethod

class Scraper(ABC):

    csv_header = ["Job Title", "Company", "Location", "Description", "Link"]

    def has_blacklisted_word(self, title, blacklisted_words): 
        for word in title.lower().split():
            if word in blacklisted_words:
                return True
            return False

    def has_city(self, city, accepted_cities):
        for word in city.lower().split():
            if word in accepted_cities:
                return True
        return False

    def sleep(self, seconds):
        time.sleep(seconds)
        return True

    def refers_language(self, requirement, languages_accepted):
        for word in requirement.lower().split():
            re.sub("([\,\s\(\)\.\;])+", "", word)
            if word in languages_accepted:
                return True
        return False

    def save_as_csv(self, job_list):
        with open("jobs2.csv", 'w', newline="", encoding="UTF-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames= self.csv_header)
            writer.writeheader()
            writer.writerows(job_list)

    @abstractmethod
    def filter_job_listing(self, element):
        pass

    @abstractmethod
    def do_job_description_refers_language(self, job, wait):
        pass

    @abstractmethod
    def transform_job_to_csv_line(self, job, driver):
        pass

    @abstractmethod
    def scrape(self):
        pass