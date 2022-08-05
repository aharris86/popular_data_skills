import numpy as np
import pandas as pd
import re
import os
import popular_data_skills.config.config as config
import popular_data_skills.utils.keywords as kws

keywords = kws.Keywords()
keywords.read_file(config.KEYWORDS)

# Get all files in data file folder
file_list = os.listdir(config.SCRAPED_DATA_FOLDER)

# Loop through files and concat to create one large data frmae.
df = pd.DataFrame()
for file in file_list:
    csv_file = config.SCRAPED_DATA_FOLDER + '\\' + file
    temp_df = pd.read_csv(csv_file)
    df = pd.concat([df, temp_df], ignore_index=True)

df.drop(['Unnamed: 0'], axis=1, inplace=True)
# Drop unusefule columns
df.drop(['work_type', 'level', 'company_info'], axis=1, inplace=True)

# Remove df values from tuples
columns = list(df.columns)
for column in columns:
    df[column] = df[column].apply(lambda x: re.sub(r"[('|',)]", '', str(x)))

# Remove 'applicants' string from applicant_count column
df = df.astype(str)
df['applicant_count'] = df['applicant_count'].apply(
    lambda x: re.sub(r" applicants", '', str(x)))

# Change strings to floats
df['applicant_count'] = pd.to_numeric(df['applicant_count'], errors='coerce')

# Convert all the strings to lower case to improve searches
columns_lower = df.columns != 'applicant_count'
df.loc[:, columns_lower] = df.loc[:,
                                  columns_lower].applymap(lambda x: x.lower())


# Delete any reposted jobs entries with the same title and same company name
df.drop_duplicates(subset=['job_title', 'company_name'],
                   inplace=True, ignore_index=True)

# Drop any duplicated job descriptions
df.drop_duplicates('job_description_lines', inplace=True, ignore_index=True)

# Remove enties from varisity tutors
df = df[df['company_name'] != 'varsity tutors a nerdy company']


# Create a filter df with keywords in the title and a df with all other entries.
analyst_words = ['analytics', 'analyst', 'analysis']
matches_regex = "|".join(analyst_words)
mask = df['job_title'].str.contains(matches_regex, regex=True)
analyst_df = df[mask].copy()
not_analyst_df = df[~mask]

# Filtering for scientist jobs
scientist_words = ['science', 'scientist', 'scientiest', 'machine learning']
matches_regex = "|".join(scientist_words)
mask = df['job_title'].str.contains(matches_regex, regex=True)
scientist_df = df[mask].copy()
not_scientist_df = df[~mask]

# Change new job values
scientist_df['job'] = 'scientist'
analyst_df['job'] = 'analyst'

# Concat filtered df into new df
df = pd.concat([scientist_df, analyst_df], ignore_index=True)

# Find 'experience' in each 'job_description_lines' and return the digit before
pattern = re.compile(
    r"((\d)|(\d )|(few ))([A-Za-z0-9\'`+]+ )([A-Za-z0-9\+]+ )(?:[A-Za-z0-9\+]+ ){0,6}experience")
df['experience'] = df['job_description_lines'].apply(
    lambda x: re.findall(pattern, x))


def extract_string(x):
    # If list is empty no numerical reference to experience was found
    if len(x) == 0:
        return np.nan

   # Loop through list of tuples
    for tuple_x in x:
        # Loop through tuple and strip white space from all strings
        y = tuple(word.strip() for word in tuple_x)
        # search for months and years in tuples if found break loop
        if ('years' in y) or ('year' in y) or ('yr' in y):
            # Some enteries state a few years this is taken as 2.
            if y[0] == 'few':
                y = 2
                break
            else:
                y = y[0]
                break

        elif ('month' in y) or ('months' in y) or ('months+' in y):
            y = 0
            break

        else:
            y = np.nan
    return y


df['experience'] = df['experience'].apply(lambda x: extract_string(x))
df['experience'] = pd.to_numeric(df['experience'], errors='coerce')

df['experience'].unique()


# Drop na lines from job description column
df.dropna(subset=['job_description_lines'], inplace=True)


# Add spaces to either side of the word
def add_spaces(keyword_dict: dict):
    """Adds one space either side of every string in a dict of lists. 

    Args:
        keyword_dict (dict): _description_

    Returns:
        spaced_kewords (dict): _description_
    """
    spaced_keywords = {}
    for key, word_list in keyword_dict.dict.items():
        # Add spaces in keyword
        spaced_key = key.center(len(key)+2)
        spaced_words_list = []
        for word in word_list:
            # Add spaces to each similar word
            spaced_word = word.center(len(word)+2)
            spaced_words_list.append(spaced_word)
        spaced_keywords[spaced_key] = spaced_words_list
    return spaced_keywords


spaced_keywords = add_spaces(keywords)

# Create df from dict of keywords and similar words
df_from_dict = pd.DataFrame()

for new_keyword, similar_words in spaced_keywords.items():
    if len(similar_words) > 0:
        pattern = '|'.join(similar_words)
        pattern = pattern + '|' + new_keyword
    else:
        pattern = new_keyword
    df_from_dict[new_keyword] = df['job_description_lines'].str.contains(
        pattern, regex=True)
    df_from_dict[new_keyword] = df_from_dict[new_keyword].astype(int)

df_from_dict.head()

# Merge from_dict_df and df to get a complete df we can save and use fro further analysis
final_df = pd.merge(df, df_from_dict, left_index=True, right_index=True)
# strip trailing and leading whitespace used in regex patterns
final_df.columns = final_df.columns.str.strip()


def add_degree(row):
    if row['phd'] == 1:
        return 'phd'
    elif row['masters degree'] == 1:
        return 'ms'
    elif row['bachelor degree'] == 1:
        return 'bs'
    elif row['degree'] == 1:
        return 'any'
    else:
        return 'not specified'


final_df['degree_level'] = final_df.apply(add_degree, axis=1)


def group_experience(row):
    if row['experience'] == 0:
        return '0'
    elif row['experience'] == 1:
        return '1'
    elif row['experience'] == 2:
        return '2'
    elif (row['experience'] >= 3) & (row['experience'] < 5):
        return '3-5'
    elif row['experience'] >= 5:
        return '5+'
    else:
        return '0'


final_df['experience'] = final_df.apply(group_experience, axis=1)
