# In Demand Data Skills

Badges

![](https://github.com/aharris86/popular_data_skills/blob/master/popular_data_skills/utils/gif-dashboard.gif)

<H3> Overview </H3>
Run an interactive dashboard to find the most in demand data skills take from linked in job listing.
The dashboard is interactive and filterable enter your job profile find most in demand skills and compare then to another job profile.

---

## Project Description

Starting out in a data role can be difficult there are so many languages and skills to learn.
Every tool comes with advantages and disadvantages.  Knowing what to focus and learn can be difficult.
There are thousands of videos and courses with contradicting inforamtion.
As the end goal is to become employed. Why not let your potential employers tell you what to learn.

Enter your job profile (job, experience, degree) and this dashboard filters linked in job posts relevant to your job profile.
Then it provides the most in demand skills mentioned in those posts.
You can also compare your job profile with a second profile. You can compare profiles to see what skills you need to level up.
If i change from analyst to scientist, what skills i need to learn now for the future.

## How it works

Selium and Beaustiful soup are used to scrape linked in job listings for relevant job posts, which are then saved.
The scraped data is wrangled into a data frame. A seperate custom  keywords module has two structures on lists all
keywords in a dictionary with a list of similar words as values. The next collects all keyords into group with groups as keys and
lists of keywords as values. Each job post is search to return if the keyword is present.
This dataframe is then filtered by the job profile variables and each skill is summed.

## Future works

Automate web scrapers - allows periodic update of job listings
Add wages information for each job profile
Add more jobs to selection - data engineer, junior roles ect
Scrape more sites - Indeed, glassdoor etc

## How to Contribute

Any and all contributions are welcome.
I am just staring out, so any

- Improvements to the code
- Improvements to keywords
- New features
- Bug reporting

Pull requests are the best way to propose changes to the codebase:
Fork the repository and create your branch from master.
Make sure your code lints.
Issue that pull request!
Note - to import and use subpackages you must install the editable version of the package to allow for updates without reinstalling the package each time.
This is in the requirements file as -e git+https://github.com/...
The config folder is used to change user information change your linked in username and password and filepaths to save csv and keywords.txt file.

## How to use

To run the dashboard run the main.py script in the root folder.
To run the webscraper - first enter your linked in username and password in the config folder.
Next run the web_scrapers_linkedin_scraper.py

## Licience

MIT Licence
