import requests
from bs4 import BeautifulSoup
import pandas as pd

position = "data scientist"
location = "United States"
# formating to linkedin model
position = position.replace(' ', "_")
location = location.replace(' ', "_")
description_file_name = fr"/most_in-demand-skills/data\indeed_{position}_{location}.csv"
position = position.replace(' ', "+")
location = location.replace(' ', "+")
url = f"https://www.indeed.com/jobs?q={position}&l={location}"
api_url = "https://www.indeed.com/viewjob?viewtype=embedded&jk={job_id}"

soup = BeautifulSoup(requests.get(url,).content, "html.parser")

for job in soup.select('a[id^="job_"]'):
    job_id = job["id"].split("_")[-1]
    s = BeautifulSoup(
        requests.get(api_url.format(job_id=job_id),).content,
        "html.parser",
    )
    try:
        job_title = soup.h1.contents[0]
    except AttributeError:
        job_title = ''
    try:
        company_name = (soup.find('a')).string
    except AttributeError:
        company_name = ''
    try:
        salary_jobtype = (soup.find("div", {"id": "salaryInfoAndJobType"})).text
    except AttributeError:
        salary_jobtype = ''
    try:
        text = soup.find("div", {"id": "jobDescriptionText"}),
    except AttributeError:
        text = ''
    try:
        bold = [b.string for b in text.findAll('b')],
    except AttributeError:
        bold = ''
    try:
        text_lists = [li.string for li in text.findAll('li')]
    except AttributeError:
        text_lists  = ''

    all_descriptions=[]

    company_des= {}

    company_des['job_title'] = job_title
    company_des['company_name'] = company_name
    company_des['salary_jobtype'] = salary_jobtype
    company_des['text'] = text
    company_des['bold_text'] = bold
    company_des['text_lists'] = text_lists

    all_descriptions.append(company_des)
    print(company_des)

    # save csv of all jobs
df = pd.DataFrame(all_descriptions)
df.to_csv(description_file_name, encoding='utf-8-sig')



# try:
#     company_des['company_name'] = soup.find("span",
#                                             attrs={'class': 'jobs-unified-top-card__company-name'}).text.strip(),
# except:
#     company_des['company_name'] = None
# try:
#     company_des['location'] = soup.find("span", attrs={'class': 'jobs-unified-top-card__bullet'}).text.strip(),
# except:
#     company_des['location'] = None
# try:
#     company_des['work_type'] = soup.find("span", attrs={'class': 'jobs-unified-top-card__workplace-type'}).text.strip(),
# except:
#     company_des['work_type'] = None
# try:
#     company_des['date_posted'] = soup.find("span",
#                                            attrs={'class': 'jobs-unified-top-card__posted-date'}).get_text().strip(),
# except:
#     company_des['date_posted'] = None
# try:
#     company_des['applicant_count'] = soup.find("span", attrs={
#         'class': 'jobs-unified-top-card__applicant-count'}).get_text().strip(),
# except:
#     company_des['applicant_count'] = None
# try:
#     company_des['level'] = texts[10].get_text().strip(),
# except:
#     company_des['level'] = None
# try:
#     company_des['company_info'] = texts[11].get_text().strip(),
# except:
#     company_des['company_info'] = None
# try:
#     company_des['job_description_lines'] = job_description.get_text()
# except:
#     company_des['job_description_lines'] = None