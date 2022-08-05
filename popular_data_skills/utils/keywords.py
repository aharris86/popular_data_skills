# Class for keywords list
# colum names are kewords and rows are similar words

from collections import UserDict
import json

path = 'dataSkills\data\processed_data\keywords.txt'


class Keywords(UserDict):
    '''
    Creates a dict on lists object to store keywords by groups or by similar words.
    Keyword = dict key - is the title keyword or title of group
    Group = dict value - are the associated words with that group given as a list
    '''

    def __init__(self):
        self.dict = dict()

    def read_dict(self, dict):
        ''' Create new object from dictionary'''
        self.dict = dict

    def read_list(self, new_list: list):
        '''
        Create new object from list. List items are keys in new object and values are an empty list.
        '''
        self.dict = dict.fromkeys(new_list, [])

    def read_file(self, path):
        ''' Opens saved json file as dict of keywords'''
        with open(path) as file:
            self.dict = json.loads(file.read())

    def save(self, path):
        '''Saves dict to txt file as json'''
        with open(path, 'w') as file:
            file.write(json.dumps(self.dict))

    def delete_keyword(self, words: list):
        '''Searches for keywords and deletes key and values for given keyword'''
        for word in words:
            del self.dict[word]

    def add_similar_words(self, new_dict):
        for keyword, similar_words in new_dict.items():
            sim_word_list = []
            if keyword in self.dict.keys():
                sim_word_list = list(set(self.dict[keyword] + similar_words))
                self.dict[keyword] = sim_word_list
            else:
                self.dict[keyword] = similar_words

    # def add_keywords(self, new_keywords):
    #     ''' Add new keyword and associated group or appends group words if keyword is in existing dict.'''
    #     # If word is not in dict add word
    #     # Use keys list to interate though dict to be able to delete and edit dict.
    #     keys_lists = self.dict.keys()
    #     for keyword, similar_words in new_keywords.items():
    #         if keyword not in self.dict.keys():
    #             self.dict[keyword] = similar_words
    #         else:
    #             old_sim_word_list = self.dict[keyword]
    #             # If word is in dict add group words to existing keyword

    #             temp_dict = {keyword: similar_words}
    #             # Add group words to keywords - using helper function
    #             self.add_similar_words(temp_dict)
    #         temp1_dict = {keyword: similar_words}
    #         # Check if any group words are in keywords - using helper function
    #         self.check_sim_words_in_keywords(temp1_dict)
    def add_keywords(self, new_keywords):
        for keyword, new_word_list in new_keywords.items():
            temp_dict = {keyword: new_word_list}
            if keyword not in self.dict.keys():
                self.dict[keyword] = new_word_list
            else:
                self.add_similar_words(temp_dict)

            self.check_sim_words_in_keywords(temp_dict)

    # def add_similar_words(self, dict):
    #     ''' Add group words to existing group words'''
    #     for keyword, similar_words in dict.items():
    #         sim_word_list = []
    #         # if keyword is in existing dict
    #         if keyword in self.dict.keys():
    #             sim_word_list = self.dict[keyword]
    #             # iterate though group words and add any new values to list
    #             for sim_word in similar_words:
    #                 if sim_word not in sim_word_list:
    #                     sim_word_list.append(sim_word)
    #             self.dict[keyword] = sim_word_list

    def delete_similar(self, new_dict: dict):
        '''Delete word in group words for existing keyword in object.'''
        for key, similar_words in new_dict.items():
            sim_word_list = self.dict[key]
            # Remove all words from exisiting group words
            for sim_word in similar_words:
                sim_word_list.remove(sim_word)
            self.dict[key] = sim_word_list

    # def check_sim_words_in_keywords(self, dict):
    #     ''' Check if any group words are in keywords. If so, add keyword and its group words to group words '''
    #     for keyword, similar_words in dict.items():
    #         sim_words_list = []
    #         for sim_word in similar_words:
    #             # Allows keyword to be in group words
    #             if sim_word != keyword:
    #                 # If group word is in keywords, add existing keyword and group into new keyword group
    #                 if sim_word in self.dict.keys():
    #                     sim_words_list = self.dict[sim_word]
    #                     dict = {keyword: sim_words_list}
    #                     self.add_similar_words(dict)
    #                     del self.dict[sim_word]

    def check_sim_words_in_keywords(self, new_dict):
        for keyword, similar_words_list in new_dict.items():
            keywords_to_delete = []
            new_words_list = similar_words_list

            for word in similar_words_list:
                if word != keyword:
                    if word in self.dict.keys():
                        new_words_list.extend(self.dict[word])
                        keywords_to_delete.append(word)
            unique_list = list(set(new_words_list))
            self.dict[keyword] = unique_list

        for word in keywords_to_delete:
            del self.dict[word]

    def combine_keywords(self, new_dict: dict):
        '''Combine two or more keywords as similar words together
        new_dict key: new keyword for combined group
        new_dict values: existing keywords to combine
        '''
        for new_key, olds_keys in new_dict.items():
            similar_words_list = []
            for old_key in olds_keys:
                for similar_word in self.dict[old_key]:
                    similar_words_list.append(similar_word)
            self.dict[new_key] = similar_words_list
            for old_key in olds_keys:
                del self.dict[old_key]
