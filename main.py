import pdb
import re
import time
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
    wait.until(lambda d: d.find_element(By.CLASS_NAME,"ot-sdk-container"))
    cookie_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
    if cookie_button:
        cookie_button.click()
        sleep(3)


def main():
    chrome.get("https://nl.indeed.com/jobs?q=Backend+Developer&l=Amsterdam&fromage=7")
    wait = WebDriverWait(chrome, timeout=20)
    final_job_list = []

    accept_cookie(chrome, wait)

    jobs = chrome.find_elements(By.CLASS_NAME, "resultContent")
    filtered_jobs = list(filter(filter_div,jobs))
    for job in filtered_jobs[:4]:
        job.find_element(By.CLASS_NAME, "jcs-JobTitle").click()
        try:
            description = wait.until(lambda c: c.find_element(By.CLASS_NAME,"jobsearch-JobComponent"))
            job_requirements = description.find_elements(By.TAG_NAME,"li")
            requirement_list = list(map(lambda x: x.text, job_requirements))
            for requirement in requirement_list:
                if refers_language(requirement):
                    final_job_list.append(job)
        except exceptions.TimeoutException:
            print(f"didn't find description for {job.text}")
    
        sleep(3)

main()
