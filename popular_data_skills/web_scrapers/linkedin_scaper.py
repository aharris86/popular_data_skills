from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import date
from dataSkills.utils.user_info import User_info as User



TODAY = str(date.today())

# Linked in username and password
user = User()
EMAIL = user.email
PASSWORD = user.password

# Linked in use geoids in the URL when searching by location.
# Geoids varibles
GEOID_UK = 101165590
GEOID_USA = 103644278

#--- ENTER SEARCH QUERY ---#
# Enter search terms to search linked in job posts
position = "entry level data scientist"
# Choose location from "United Kingdom" or "United States"
location = "United States"

# Select geoid to add to url depending on location
if location == "United States":
    geoid = GEOID_USA
elif location == "United Kingdom":
    geoid = GEOID_UK

# Edit search terms to add to file name of saved csv
position_for_file = position.replace(' ', "_")
location_for_file = location.replace(' ', "_")
file_name = fr"/dataSkills\data\scraped_data\{TODAY}_{position_for_file}_{location_for_file}_scraped.csv"

# Create URL for searching job posts
#scrape_page_url= f"https://www.linkedin.com/jobs/search/?currentJobId=3056584651&f_E=1%2C2&f_WT=2&geoId=103644278&keywords=junior%20python&location=United%20States"
position = position.replace(' ', "+")
location = location.replace(' ', "+")
scrape_page_url= f"https://www.linkedin.com/jobs/search/?keywords={position}&location={location}&locationId=&geoId={geoid}&f_TPR=&f_E=1%2C2&f_WT=2"

 # https://www.linkedin.com/jobs/search/?keywords=entry+level+data+scientist&location=United+States&locationId=&geoId=103644278&f_TPR=&f_E=1%2C2&f_WT=2


# Initiate Webdriver
options = Options()
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.set_window_size(1024, 600)

# Opening linkedin website
driver.get("https://www.linkedin.com/login")

time.sleep(2)

# Enter credentials
driver.find_element(By.ID, 'username').send_keys(EMAIL)
driver.find_element(By.ID, 'password').send_keys(PASSWORD)
driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)

driver.get(scrape_page_url)
driver.maximize_window()
time.sleep(2)

# There are varying post for each search.
# Create a nested loop
# First loops through search pages
# Second loops through job posts on each page
# When there are no more elements the loop breaks

# List to store scraped job posts
all_descriptions = []


for i in range(1, 30):
    # click button to change page
    try:
        driver.find_element(By.XPATH, f"/ html / body / div[6] / div[3] / div[3] / div[2] / div / section[1] / div / div / ul / li[{i}] / div / div[1] / div[1] / div[2] / div[1] / a").click()
    except NoSuchElementException:
        print('break1')
        break

    # The number of job post on each page is not consistent
    # Get list of jobs to find total jobs on each page
    try:
        jobs_lists = driver.find_element(By.CLASS_NAME, "jobs-search-results__list")
        jobs = jobs_lists.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')
    except NoSuchElementException:
        print('break2')
        break
    time.sleep(1)

    # loop through job posts on page and scrape info
    for job in range(1, len(jobs)+1):

        # job click
        try:
            driver.find_element(By.XPATH, f'/ html / body / div[6] / div[3] / div[3] / div[2] / div / section[1] / div / div / ul / li[{job}] / div / div[1] / div[1] / div[2] / div[1] / a').click()
            # / html / body / div[6] / div[3] / div[3] / div[2] / div / section[1] / div / div / ul / li[{job}] / div / div[1] / div[1] / div[2] / div[1] / a
            # / html / body / div[6] / div[3] / div[3] / div[2] / div / section[1] / div / div / ul / li[2] / div / div[1] / div[1] / div[2] / div[1] / a
        except NoSuchElementException:
            print("No element")
            break
        except StaleElementReferenceException:
            break

        time.sleep(1)

        # Get job description
        try:
            job_desc = driver.find_element(By.CLASS_NAME, 'jobs-search__right-rail')
        except NoSuchElementException:
            print("No right rail")
            break

        # Scrape text with Beautiful soup
        soup = BeautifulSoup(job_desc.get_attribute(
            'outerHTML'), 'html.parser')
        texts = soup.find_all("span")

        # Store scraped post info in a dict
        company_des = {}

        try:
            company_des['job_title'] = soup.find("h2").text.strip(),
        except:
            company_des['job_title'] = None
        try:
            company_des['company_name'] = soup.find("span", attrs={'class' : 'jobs-unified-top-card__company-name'}).text.strip(),
        except:
            company_des['company_name'] = None
        try:
            company_des['location'] = soup.find("span", attrs={'class' : 'jobs-unified-top-card__bullet'}).text.strip(),
        except:
            company_des['location']= None
        try:
            company_des['work_type'] = soup.find("span", attrs={'class' : 'jobs-unified-top-card__workplace-type'}).text.strip(),
        except:
            company_des['work_type']= None
        try:
            company_des['date_posted'] = soup.find("span", attrs={'class' : 'jobs-unified-top-card__posted-date'}).get_text().strip(),
        except:
            company_des['date_posted']= None
        try:
            company_des['applicant_count'] = soup.find("span", attrs={'class' : 'jobs-unified-top-card__applicant-count'}).get_text().strip(),
        except:
            company_des['applicant_count']= None
        try:
            company_des['level'] = texts[10].get_text().strip(),
        except:
            company_des['level']= None
        try:
            company_des['company_info'] = texts[11].get_text().strip(),
        except:
            company_des['company_info']= None

        job_description = texts[-1]
        try:
            company_des['job_description_lines'] = job_description.get_text()
        except:
            company_des['job_description_lines']= None
            
        if location.lower() == 'united states':
            company_des['country'] = 'usa'
        elif location.lower() == 'united kingdom':
            company_des['country'] = 'uk'
            
        if (position.lower() == 'science') or (position.lower() == 'scientist'):
            company_des['job'] = 'scientist'
        elif (position.lower() == 'analysis') or (position.lower() == 'analyst'):
            company_des['job'] = 'analyst'
            

        all_descriptions.append(company_des)
        print(company_des)

# save csv of all jobs
df = pd.DataFrame(all_descriptions)
df.to_csv(file_name)


