from selenium import webdriver
from indeed_scraper import IndeedScraper
from glassdoor_scraper import GlassdoorScraper
CSV_HEADER = ["Job Title", "Company", "Location", "Description", "Link"]

JOB_TITLE = "Backend Developer"
LOCATION = "Amsterdam"
accepted_cities = {"amsterdam", "utrecht", "rotterdam", "hoofddorp", "diemen"}
blacklisted_words = {"senior", "lead", "php", "full-stack", "fullstack"}
languages_accepted = {"java", "python"}

def main():
    chrome = webdriver.Chrome()
    indeed_scraper = IndeedScraper(JOB_TITLE, LOCATION, blacklisted_words, accepted_cities, languages_accepted, chrome)
    indeed_scraper.scrape()
    glassdoor_scraper = GlassdoorScraper(JOB_TITLE, LOCATION, blacklisted_words, accepted_cities, languages_accepted, chrome)
    glassdoor_scraper.scrape()


main()
