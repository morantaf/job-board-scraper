import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.wait import WebDriverWait
from scraper import Scraper


class IndeedScraper(Scraper):

    def __init__(self, job_title, location, blacklisted_words, accepted_cities, languages_accepted, chrome):
        self.chrome = chrome
        self.job_title = job_title.replace(" ","+")
        self.location = location
        self.blacklisted_words = blacklisted_words
        self.accepted_cities = accepted_cities
        self.languages_accepted = languages_accepted
        self.filename = "indeed-jobs.csv"

    def filter_job_listing(self, element):
        title = element.find_element(By.CLASS_NAME, "jcs-JobTitle").text
        city = element.find_element(By.CLASS_NAME, "companyLocation").text

        if not self.has_city(city, self.accepted_cities) or self.has_blacklisted_word(title, self.blacklisted_words):
            return False
        return True

    def reject_cookie(self, driver, wait):
        cookie_popup = wait.until(lambda d: d.find_elements(By.CLASS_NAME, "ot-sdk-container"))
        if len(cookie_popup) > 0:
            cookie_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
            cookie_button.click()


    def transform_job_to_csv_line(self, job, driver):
        line = {}
        link = job.find_element(By.CLASS_NAME, "jcs-JobTitle").get_attribute("href")
        right_pane = driver.find_element(By.CLASS_NAME, "jobsearch-JobComponent")
        title = right_pane.find_element(By.CSS_SELECTOR, ".jobsearch-JobInfoHeader-title.is-embedded").text
        company = right_pane.find_element(By.CSS_SELECTOR, ".css-1cjkto6").text
        city = right_pane.find_element(By.CSS_SELECTOR, ".css-6z8o9s").text
        description = right_pane.find_element(By.ID, "jobDescriptionText").text
        line[self.csv_header[0]] = title
        line[self.csv_header[1]] = company
        line[self.csv_header[2]] = city
        line[self.csv_header[3]] = description
        line[self.csv_header[4]] = link

        return line


    def close_popups(self, driver):
        if len(driver.find_elements(By.ID, "google-Only-Modal")) > 0:
            driver.find_element(By.CLASS_NAME, "icl-CloseButton").click()
        if len(driver.find_elements(By.ID, "mosaic-desktopserpjapopup")) > 0:
            driver.find_element(By.CSS_SELECTOR, ".css-yi9ndv").click()


    def save_as_csv(self, job_list, filename):
        with open(filename, 'w', newline="", encoding="UTF-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.csv_header)
            writer.writeheader()
            writer.writerows(job_list)


    def scrape(self,):
        self.chrome.get(f"https://nl.indeed.com/jobs?q={self.job_title}&l={self.location}&fromage=7")
        wait = WebDriverWait(self.chrome, timeout=20)
        job_list = []

        self.reject_cookie(self.chrome, wait)

        continue_navigation = True

        while continue_navigation:
            self.sleep(2)
            self.close_popups(self.chrome)
            jobs = self.chrome.find_elements(By.CLASS_NAME, "resultContent")
            filtered_jobs = list(filter(self.filter_job_listing, jobs))
            for job in filtered_jobs:
                try:
                    job.find_element(By.CLASS_NAME, "jcs-JobTitle").click()
                    description = wait.until(lambda c: c.find_element(By.CLASS_NAME, "jobsearch-JobComponent"))
                    if self.do_job_description_refers_language(description, self.languages_accepted):
                        csv_line = self.transform_job_to_csv_line(job, self.chrome)
                        job_list.append(csv_line)
                    self.sleep(3)
                except exceptions.TimeoutException:
                    title = description.find_element(By.CSS_SELECTOR, ".jobsearch-JobInfoHeader-title.is-embedded").text
                    print(f"didn't find description for {title}")

            pagination_buttons = self.chrome.find_elements(By.CSS_SELECTOR, ".css-13p07ha")
            if len(pagination_buttons) > 0:
                last_button = pagination_buttons[-1]
                if last_button.get_attribute("data-testid") == "pagination-page-next":
                    last_button.click()
                else:
                    continue_navigation = False
            else:
                continue_navigation = False

        if len(job_list) > 0:
            self.save_as_csv(job_list, self.filename)

if __name__ == "__main__":
    chrome = webdriver.Chrome()
    indeed_scraper = IndeedScraper(main.JOB_TITLE, main.LOCATION, main.blacklisted_words, main.accepted_cities, main.languages_accepted, chrome)
    indeed_scraper.scrape()