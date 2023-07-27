import pdb
import main
from scraper import Scraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

class GlassdoorScraper(Scraper):
    
    def __init__(self, job_title, location, blacklisted_words, accepted_cities, languages_accepted, chrome):
        self.chrome = chrome
        self.job_title = job_title.lower().replace(" ","-")
        self.location = location.lower()
        self.blacklisted_words = blacklisted_words
        self.accepted_cities = accepted_cities
        self.languages_accepted = languages_accepted
        self.filename = "glassdoor-jobs.csv"

    def accept_cookie(self, driver, wait):
        cookie_popup = wait.until(lambda d: d.find_elements(By.CLASS_NAME, "ot-sdk-container"))
        if len(cookie_popup) > 0:
            cookie_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
            cookie_button.click()

    def filter_job_listing(self, element):
        title = element.find_element(By.CLASS_NAME, "job-title").text
        city = element.find_element(By.CLASS_NAME, "location").text

        if not self.has_city(city, self.accepted_cities) or self.has_blacklisted_word(title, self.blacklisted_words):
            return False
        return True

    def click_show_more(self, description):
        show_more = description.find_element(By.CLASS_NAME, "css-t3xrds")
        show_more.click()
    
    def transform_job_to_csv_line(self, job, driver):
        line = {}
        link = job.find_element(By.TAG_NAME, "a").get_attribute("href")
        right_pane = driver.find_element(By.ID, "JDCol")
        title = right_pane.find_element(By.CSS_SELECTOR, ".css-w04er4 .e1tk4kwz4").text
        company = right_pane.find_element(By.CSS_SELECTOR, ".css-87uc0g").text
        city = right_pane.find_element(By.CSS_SELECTOR, ".css-56kyx5").text
        description = right_pane.find_element(By.CLASS_NAME, "jobDescriptionContent").text
        line[self.csv_header[0]] = title
        line[self.csv_header[1]] = company
        line[self.csv_header[2]] = city
        line[self.csv_header[3]] = description
        line[self.csv_header[4]] = link

        return line

    def bypass_login(self, driver):
        login_popup = driver.find_elements(By.ID, "LoginModal")
        if len(login_popup) > 0 and login_popup[0].get_attribute("innerHTML") != "":
            close_button = login_popup[0].find_elements(By.TAG_NAME, "button")[0]
            close_button.click()

    def scrape(self):
        self.chrome.get(f"https://www.glassdoor.com/Job/{self.location}-{self.job_title}-jobs-SRCH_IL.0,9_IC3064478_KO10,27.htm?fromAge=14")
        wait = WebDriverWait(self.chrome, timeout=20)
        job_list = []
        self.accept_cookie(self.chrome, wait)

        continue_navigation = True

        while continue_navigation:
            self.sleep(2)
            jobs_listing = self.chrome.find_elements(By.CLASS_NAME, "react-job-listing")
            
            filtered_jobs = list(filter(self.filter_job_listing, jobs_listing))

            for job in filtered_jobs:
                self.sleep(1)
                job.click()
                self.bypass_login(self.chrome)
                description = wait.until(lambda c: c.find_element(By.ID, "JobDescriptionContainer"))
                self.click_show_more(description)
                self.sleep(2)

                if self.do_job_description_refers_language(description, self.languages_accepted):
                    csv_line = self.transform_job_to_csv_line(job, self.chrome)
                    job_list.append(csv_line)
                    self.sleep(3)
            
            next_button = self.chrome.find_element(By.CLASS_NAME, "nextButton")
            if next_button.is_enabled():
                next_button.click()
            else:
                continue_navigation = False

        if len(job_list) > 0:
            self.save_as_csv(job_list, self.filename)
                

if __name__ == "__main__":
    chrome = webdriver.Chrome()
    glassdoor_scraper = GlassdoorScraper(main.JOB_TITLE, main.LOCATION, main.blacklisted_words, main.accepted_cities, main.languages_accepted, chrome)
    glassdoor_scraper.scrape()