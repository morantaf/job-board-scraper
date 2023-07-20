import re
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.wait import WebDriverWait

chrome = webdriver.Chrome()

ACCEPTED_CITIES = {"amsterdam", "utrecht", "rotterdam", "hoofddorp"}
BLACKLISTED_WORDS = {"senior", "lead", "php", "full-stack", "fullstack"}
LANGUAGES_DESIRED = {"java", "python"}
CSV_HEADER = ["Job Title", "Company", "Location", "Description", "Link", "Source"]


def has_blacklisted_word(title):
    for word in title.lower().split():
        if word in BLACKLISTED_WORDS:
            return True
    return False


def has_city(location):
    for word in location.lower().split():
        if word in ACCEPTED_CITIES:
            return True
    return False


def filter_div(div):
    title = div.find_element(By.CLASS_NAME, "jcs-JobTitle").text
    location = div.find_element(By.CLASS_NAME, "companyLocation").text

    if not has_city(location) or has_blacklisted_word(title):
        return False
    return True


def refers_language(requirement):
    for word in requirement.lower().split():
        re.sub("([\,\s\(\)\.\;])+", "", word)
        if word in LANGUAGES_DESIRED:
            return True
    return False

# Used to slow down the execution to bypass the anti-bot protection


def sleep(seconds):
    time.sleep(seconds)
    return True


def accept_cookie(driver, wait):
    cookie_popup = wait.until(lambda d: d.find_elements(By.CLASS_NAME, "ot-sdk-container"))
    if len(cookie_popup) > 0:
        cookie_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
        cookie_button.click()


def do_job_refers_language(job, wait):
    job.find_element(By.CLASS_NAME, "jcs-JobTitle").click()
    try:
        description = wait.until(lambda c: c.find_element(By.CLASS_NAME, "jobsearch-JobComponent"))
        job_requirements = description.find_elements(By.TAG_NAME, "li")
        requirement_list = list(map(lambda x: x.text, job_requirements))
        for requirement in requirement_list:
            if refers_language(requirement):
                return True
    except exceptions.TimeoutException:
        print(f"didn't find description for {job.text}")
    return False


def transform_job_to_csv_line(job, driver):
    line = {}
    link = job.find_element(By.CLASS_NAME, "jcs-JobTitle").get_attribute("href")
    right_pane = driver.find_element(By.CLASS_NAME, "jobsearch-JobComponent")
    job_title = right_pane.find_element(By.CSS_SELECTOR, ".jobsearch-JobInfoHeader-title.is-embedded").text
    company = right_pane.find_element(By.CSS_SELECTOR, ".css-1cjkto6").text
    location = right_pane.find_element(By.CSS_SELECTOR, ".css-6z8o9s").text
    description = right_pane.find_element(By.ID, "jobDescriptionText").text
    line[CSV_HEADER[0]] = job_title
    line[CSV_HEADER[1]] = company
    line[CSV_HEADER[2]] = location
    line[CSV_HEADER[3]] = description
    line[CSV_HEADER[4]] = link

    return line


def close_popups(driver):

    if len(driver.find_elements(By.ID, "google-Only-Modal")) > 0:
        driver.find_element(By.CLASS_NAME, "icl-CloseButton").click()
    if len(driver.find_elements(By.ID, "mosaic-desktopserpjapopup")) > 0:
        driver.find_element(By.CSS_SELECTOR, ".css-yi9ndv").click()


def save_as_csv(job_list):
    with open("jobs.csv", 'w', newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADER)
        writer.writeheader()
        writer.writerows(job_list)


def main():
    chrome.get("https://nl.indeed.com/jobs?q=Backend+Developer&l=Amsterdam&fromage=7")
    wait = WebDriverWait(chrome, timeout=20)
    job_list = []

    accept_cookie(chrome, wait)

    while True:
        sleep(2)
        close_popups(chrome)
        jobs = chrome.find_elements(By.CLASS_NAME, "resultContent")
        filtered_jobs = list(filter(filter_div, jobs))
        for job in filtered_jobs:
            if do_job_refers_language(job, wait):
                csv_line = transform_job_to_csv_line(job, chrome)
                job_list.append(csv_line)
            sleep(3)

        pagination_buttons = chrome.find_elements(By.CSS_SELECTOR, ".css-13p07ha")
        if len(pagination_buttons) > 0:
            last_button = pagination_buttons[-1]
            if last_button.get_attribute("data-testid") == "pagination-page-next":
                last_button.click()
            else:
                break
        else:
            break

    if len(job_list) > 0:
        save_as_csv(job_list)


main()
