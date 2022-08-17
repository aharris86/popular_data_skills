![Banner](images/Popular_data_skills_analysis_banner.png)

# Popular Data Skills Analysis

# Abstract
In order to find the most requested skills on linked in job posts for data roles. 
This was done by scraping text from linked in job posts with search terms related to data roles.
Data was cleaned and wrangled to find most common words. These words were narrowed down to most common skills.
Job posts were scanned for common skills and the sum of these skills were collated into most popular skills. 
These were later filtered by degree, job and experience to find most popular skills in the sub set of data.
An acceptable learning path to best match most job posts out there could be: 
Any degree bachelors or above is acceptable.
Learn Python and SQL. 
First learn analytics using statistical methods
Next learn to visualize them well. Using both Power BI and Tableau.
Then learn to use Machine learning models and deep learning models in your analysis. 
Working with projects in Healthcare or finance will be an advantage.


## The Problem 
Data science is a broad subject with many disciplines. Creating a learning path can be confusing and frustrating.
There are many conflicting ideas about what you should learn. 

## The Proposal 
To solve this issue. A efficient and logical way to create a learning path may be to find the skills companies request the most.
This will create a job profile that will match the largest percentage of job posts.  As the skills will match the largest majority 
of job post the individual should have the greatest chance of being contacted by potential employers. 


## Assumptions 
- There are a number of assumptions taken during this project in order to keep the size of the project manageable. 
- These can be re-visited later. 
- The assumption that the goal of the individual is to get a job as soon as possible. 
- This report assumes that any job role is suitable and the individual does not want to specialise in a particular area of data science
- That matching keywords skills are sufficient to stand out ot employers and that many jobs don't ask for specific skills within that discipline 
that are not in the keywords. 
- That job posts on Linked in are representative of job post from other sites.  

### Technologies
* Python
* Pandas, jupyter
* Selenium
* Beautiful Soup
* NLTK
* Matplotlib


# Data
Data was scraped from linked in job posts using Selenium and Beautiful Soup. Search terms used were:
'data scientist', 'data analysis', 'junior data scientist', 'junior data analyst'. Searches were located in 'USA' and the 'UK'. 
raw data was then stored in a csv file using pandas. 

# Methodology & Notebooks

### Data Wrangling 
**Notebook** - [a_wrangle_data](popular_data_skills/exploratory_analysis/a_wrangle_data.ipynb)  
The raw csv file was wrangled using pandas and regex and wordcloud. 
All duplicate job posts or spam job posts(similar job posts with just a location change) were removed.
Job post titles were used to create job roles.
Regex was used to search for digits close to experience to create an experience feature. 

### Initial common words
**Notebook** - [b_common_words](popular_data_skills/exploratory_analysis/b_common_words.ipynb)   
Initial common words form the entire corpus were used to create a custom skill keyword list. 
All posts were collated and words were tokenized.  Stop words from the NLTK were removed to reduce the size of the corpus.
WordNetLemmatizer from NLTK was used to stem words as it is not as harsh as other stemming options. The main use of the stemming was to remove plurals. 

### Creating custom Keyword list
**Notebook** - [c_structuring_keywords](popular_data_skills/exploratory_analysis/c_structuring_keywords.ipynb)  
From the initial common words list. The common words list was scanned manually to select words of interest. 
Similar meaning words were collated into the same keyword. 
These keywords were then collected into groups
of similar interests. These groups are: 'Language', 'Tools', 'Degree', 'Topic', 'Skills', 'Business area'. 

**Class** - [keywords](popular_data_skills/utils/keywords.py)  
These keywords and groups were stored in a dictionary of lists.
A class was created to store, update and edit this structure to easily manage the keywords. 

### Adding features
**Notebook** - [d_adding_features](popular_data_skills/exploratory_analysis/d_adding_features.ipynb)  
Each job post was scanned for selected keywords and the results are stored in a dataframe. Totals for each keyword were used 
to calculate percentage of job posts that contain each keyword. 
The dataframe is stored as a csv in b_final_data

### Filter features 
**Notebook** - [e_filter_features](popular_data_skills/exploratory_analysis/e_filter_features.ipynb)  
This notebook prepares the data to use in the dashboard.
The data frame is filtered by the features 'job', 'experience' and 'degree'. Two different profiles can be selected to compare the different in relevant skills.
The percent of entries relative to the total of the keyword group is calculated in order to give a proportion ratio of each group.  This is easier to comprehend 
in the dashboard tree. 
Comparison bar charts and treemap were created for visual comparison. 

### Script
**Script** - [f_analysis_script](popular_data_skills/exploratory_analysis/f_analysis_script.py)  
The wrangling and feature selection was compiled into a script for easy future use.

# Results
Below are the top ten requested skills most of these are requested in over 50% of job posts.   
![Top ten Skills](popular_data_skills/images/top_ten_skills.png)     
This is a good start but these are large areas. The following images narrow down certain areas more.     
### Languages 
![Top languages](popular_data_skills/images/most_popular_languages.png)  
### Degree
![Top degree](popular_data_skills/images/most_popular_degree.png)  
### Topics
![Top topics](popular_data_skills/images/most_popular_topics.png)  
### Tools
![Top tools](popular_data_skills/images/most_popular_tools.png)   
### Skills
![Top skills](popular_data_skills/images/most_popular_skills.png)   
### Business sectors
![Top business sector](popular_data_skills/images/most_popular_business_area.png)   

# Conclusion 
This analysis proposed a different approach to structure learning the required skills to get a job in a data role.
In order to choose a learning path that will give you the skills that match 
the most requested skills in companies job posts. Hence, matching your CV to the keywords in the post.     
Any degree bachelors or above is acceptable.   
Learn Python and SQL.   
First learn analytics using statistical methods.  
Next learn to visualize them well. Using both Power BI and Tableau.  
Then learn to use Machine learning models and deep learning models in your analysis.   
Working with projects in Healthcare or finance will be an advantage.  

## Limitations 
- This project is designed as a guide only.   
- This work is limited to a small sample of approximately 600 posts. The sample size is small and from one single source(Linked in).   
- This could skew the results. Please see Future work below for possible improvements.   
- Simple keyword match has been used. Groups of consecutive words have not been considered.  
- Keywords could be better grouped into subsets to ensure groups contain sub sets of the keyword group.  
- Check keywords that are subsets of other keywords are related and counted.   
- Words have not been checked for double meanings. See Future Work below for some examples 


## Future Work  
- Automate webscraper to create larger dataset.
- Scrape information from other sites to create a more varied dataset. 
- Try other stemming techniques apart from WordNetLemmatizer
- Search for other sources of keywords. 
- Check keywords for possible double meaning ex. (Healthcare, visualize, decision trees)

