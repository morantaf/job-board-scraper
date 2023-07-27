# Job Scraper

## Origin of the project

One of the most annoying and time-consuming aspects of job hunting is having to sift through search results, wasting 
time reading through countless job descriptions, and filtering out the offers that don't fit your skillset. 
For instance, you might be looking for a Java position, only to discover at the end of the description that they're seeking a PHP developer. 
To address this issue, I came up with the idea of building a program that will filter job listings for me. 
It removes the cities, languages, and seniority levels that don't align with my preferences.

## Project Overview
The Job Scraper project is a powerful tool built for the purpose of scraping job listings from Job Board websites. It is specifically designed to search for 'Backend Developer' jobs in the Amsterdam area, but its flexible design allows it to be easily modified to search for any other job title or location.

The scraper filters the job listings based on specific criteria such as accepted cities, blacklisted words, and desired programming languages. It then compiles the collected data into CSV files for easy analysis and processing.

## Features
1. **Flexibility**: The Job Scraper can be easily modified to suit a variety of job searches. By simply altering the parameters, you can customize the job title, location, accepted cities, blacklisted words, and languages accepted.
2. **Multiple Platform Support**: The scraper works on both Indeed and Glassdoor, giving a wider range of job listings.
3. **Data Filtering**: The scraper filters out unwanted job listings based on the criteria defined, giving a more streamlined and relevant list of job opportunities.
4. **CSV Output**: The scraped job listings are saved into CSV files, making it easy for further analysis and processing.

## Getting Started

### Prerequisites
1. Python 3
2. Selenium WebDriver

### Setup
1. Clone this repository to your local machine.
2. Install the required Python packages by running the following command:

       pip install -r requirements.txt
   
4. Download the appropriate [Chrome WebDriver](https://chromedriver.chromium.org/downloads) based on your version of Chrome Browser and add it to your system path.

### Running the Scraper
1. Open the `main.py` file and adjust the `JOB_TITLE` and `LOCATION` variables to fit your desired job search.
2. Also, modify the `accepted_cities`, `blacklisted_words`, and `languages_accepted` sets as required.
3. Run `main.py` to start the scraper:

       python3 main.py

The program will start and scrape job listings based on your defined criteria.

## Expected Output
Once the scraper has finished running, it will output two CSV files: `indeed-jobs.csv` and `glassdoor-jobs.csv`. These files will contain job listings from Indeed and Glassdoor respectively, each containing the job title, company name, job location, job description, and link to the job listing.

## Current limitations

1. Hardcoded parameters: The job title, location, blacklisted words, accepted cities, and accepted languages are hardcoded into the main.py script. To change the search parameters, the user needs to manually edit the code. It would be more user-friendly if the program could accept these as inputs.
2. Limited Filtering: The current filtering criteria only include location, languages, blacklisted words, and accepted cities.
3. Rate Limiting and Blocking: Automated scraping may lead to the user's IP being rate-limited or blocked by the websites being scraped.
