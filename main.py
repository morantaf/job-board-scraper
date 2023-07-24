from indeed_scraper import IndeedScraper

CSV_HEADER = ["Job Title", "Company", "Location", "Description", "Link"]

job_title = input("Enter the job you're looking for: ")
location = input("Enter desired location: ")
accepted_cities = {"amsterdam", "utrecht", "rotterdam", "hoofddorp"}
blacklisted_words = {"senior", "lead", "php", "full-stack", "fullstack"}
languages_accepted = {"java", "python"}

def main():
    indeed_scraper = IndeedScraper(job_title, location, blacklisted_words, accepted_cities, languages_accepted)
    indeed_scraper.scrape()

main()
