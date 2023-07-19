import pdb
import re
import time
import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.wait import WebDriverWait

chrome = webdriver.Chrome()

ACCEPTED_CITIES = {"amsterdam","utrecht","rotterdam", "hoofddorp"}
BLACKLISTED_WORDS = {"senior", "lead", "php", "full-stack", "fullstack"}
LANGUAGES_DESIRED = {"java", "python"}

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
        re.sub("([\,\s\(\)\.\;])+","",word)
        if word in LANGUAGES_DESIRED:
            return True
    return False

# Used to slow down the execution to bypass the anti-bot protection
def sleep(seconds):
    time.sleep(seconds)
    return True

def accept_cookie(driver, wait):
    cookie_popup = wait.until(lambda d: d.find_elements(By.CLASS_NAME,"ot-sdk-container"))
    if len(cookie_popup) > 0:
        cookie_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
        cookie_button.click()

def do_job_refers_language(job, wait):
    job.find_element(By.CLASS_NAME, "jcs-JobTitle").click()
    try:
        description = wait.until(lambda c: c.find_element(By.CLASS_NAME,"jobsearch-JobComponent"))
        job_requirements = description.find_elements(By.TAG_NAME,"li")
        requirement_list = list(map(lambda x: x.text, job_requirements))
        for requirement in requirement_list:
            if refers_language(requirement):
                return True
    except exceptions.TimeoutException:
        print(f"didn't find description for {job.text}")
    return False

def close_popups(driver):
    
    if len(driver.find_elements(By.ID,"google-Only-Modal")) > 0:
        driver.find_element(By.CLASS_NAME, "icl-CloseButton").click()
    if len(driver.find_elements(By.ID,"mosaic-desktopserpjapopup")) > 0:
        driver.find_element(By.CSS_SELECTOR, ".css-yi9ndv").click()

def main():
    chrome.get("https://nl.indeed.com/jobs?q=Backend+Developer&l=Amsterdam&fromage=7")
    wait = WebDriverWait(chrome, timeout=20)
    final_job_list = []

    accept_cookie(chrome, wait)

    while True:
        sleep(2)
        close_popups(chrome)
        jobs = chrome.find_elements(By.CLASS_NAME, "resultContent")
        filtered_jobs = list(filter(filter_div,jobs))
        for job in filtered_jobs:
            if do_job_refers_language(job, wait):
                final_job_list.append(job)
            sleep(3)

        pagination_buttons = chrome.find_elements(By.CSS_SELECTOR,".css-13p07ha")
        if len(pagination_buttons) > 0:
            last_button = pagination_buttons[-1]
            print(last_button.get_attribute("data-testid"))
            if last_button.get_attribute("data-testid") == "pagination-page-next":
                last_button.click()
            else:
                break
        else:
            break
        
    # pprint.pprint(list(map(lambda x: x.text, final_job_list)))
    

main()
