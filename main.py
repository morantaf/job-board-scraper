import pdb
import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome = webdriver.Chrome()

ACCEPTED_CITIES = ["amsterdam","utrecht","rotterdam"]
BLACKLISTED_WORDS = ["senior", "lead", "php", "full-stack", "fullstack"]

def has_blacklisted_word(title): 
    for word in title.lower().split():
        if word in BLACKLISTED_WORDS:
            return True
    return False

def filter_div(div):
    title = div.find_element(By.CLASS_NAME, "jcs-JobTitle").text
    location = div.find_element(By.CLASS_NAME, "companyLocation").text
    if not location.lower() in ACCEPTED_CITIES and has_blacklisted_word(title):
        return False
    return True

def main():
    chrome.get("https://nl.indeed.com/jobs?q=Backend+Developer&l=Amsterdam&from=searchOnHP")
    wait = WebDriverWait(chrome, timeout=20)
    wait.until(lambda d: d.find_element(By.CLASS_NAME,"ot-sdk-container"))
    cookie_button = chrome.find_element(By.ID, "onetrust-reject-all-handler")
    if cookie_button:
        cookie_button.click()
    jobs = chrome.find_elements(By.CLASS_NAME, "resultContent")
    filtered_jobs = list(filter(filter_div,jobs))
    job = filtered_jobs[0]
    job.find_element(By.CLASS_NAME, "jcs-JobTitle").click()
    pdb.set_trace()
    description = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"jobsearch-embeddedBody")))
    # pprint.pprint(description.get_attribute("innerHTML"))
    # pprint.pprint(list(map(lambda x: x.text, lists)))
    # for job in filtered_jobs:
    #     job.find_element(By.CLASS_NAME, "jcs-JobTitle").click()
    #     wait.until(EC.presence_of_element_located((By.CLASS_NAME,"jobsearch-embeddedBody")))
    
    #print(links)

main()
