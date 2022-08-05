import popular_data_skills.utils.keywords as keywords
import popular_data_skills.config.config as config

KWS_GROUPS_PATH = r'../data/processed_data/keywords/keyword_groups.txt'

# Get lists for keywords class 
kws = keywords.Keywords()
kws.read_file(config.KEYWORD_GROUPS)

def group_list():
    return list(kws.dict.keys())


def degree_level(degree: str):
    '''Filters info to provide list of values to filter the degree column'''
    if degree == 'phd':
        return ['phd', 'ms', 'bs', 'not_specified']
    elif degree == 'ms':
        return ['ms', 'bs', 'not_specified']
    elif degree == 'bs':
        return ['bs', 'not_specified']
    elif degree == 'none':
        return ['not_specified']
    elif degree == 'any':
        return ['phd', 'ms', 'bs', 'not_specified']


def experience_level(experience :str):
    '''Filters info to provide list of values to filter the experience column'''
    if experience == '5+':
        return ['0', '1', '2', '3-5', '5+']
    elif experience == '3-5':
        return ['0', '1', '2', '3-5']
    elif experience == '2':
        return ['0', '1', '2']
    elif experience == '1':
        return ['0', '1']
    elif experience == '0':
        return ['0']

def filter_df(df,job,experience,degree):
    '''Uses Helper functions experience level and degree_level to filter df according to profile varibles'''
    df = df[
    (df['job'] == job) & 
    (df['experience'].isin(experience_level(experience))) &
    (df['degree_level'].isin(degree_level(degree)))
    ]
    return df

def add_groups(row):
    ''' Adds groups taken from imported keywords list class. Used to add new column to df to group skills together'''
    for group, list in kws.dict.items():
        if row in list: 
            return group
        
def get_group_totals(df):
    '''Create two groupby dfs from filtered info. First df shows totals count for each group. Second collates total count of each skill'''
    group_total_df = df.groupby(by='groups',as_index=False).sum()
    group_total_df.rename(columns={0:'group_total'}, inplace = True)

    grouped_df = df.groupby(['groups', 'index'],as_index=False).sum()
    grouped_df.rename(columns={0:'count'}, inplace = True)
    return group_total_df, grouped_df




    