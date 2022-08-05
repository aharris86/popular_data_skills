import os

#-------------- WEB SCRAPER --------------#

# Linked in User name and password


class User_info:
    def __init__(self):
        self.email = "**Your Linked in EMAIL here.**"
        self.password = "**Your linked in password here.**"


#-------------- DATA FILES --------------#

# ROOT_DIR gives the path to the root directory of the project
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

#------ DATA FRAMES -----#
SCRAPED_DATA_FOLDER = ROOT_DIR + r'\data\scraped_data'
WRANGLED_DATA_FILE = ROOT_DIR + r'\data\analysis_data\a_wrangled_data.csv'
FINAL_DATA_FILE = ROOT_DIR + r'\data\analysis_data\b_final_data.csv'

#----- Keywords -----#

COMMON_WORDS = ROOT_DIR + r'\data\analysis_data\keywords\a_most_common_words.txt'
SELECTED_WORDS = ROOT_DIR + r'\data\analysis_data\keywords\b_selected_words.txt'
KEYWORDS = ROOT_DIR + r'\data\analysis_data\keywords\c_keywords.txt'
KEYWORD_GROUPS = ROOT_DIR + r'\data\analysis_data\keywords\d_keyword_groups.txt'