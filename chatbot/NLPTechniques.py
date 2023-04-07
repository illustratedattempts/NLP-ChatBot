import re
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize

from CommentFinder import CommentFinder

class NLPTechniques:
    
    # Input: String of text
    # Output: List of filtered words
    def clean_text(self, text):
        # Remove \t, \r, \n
        text = re.sub(r'[\t|\r|\n]', '', text)
        # Remove all non-alphanumeric characters
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        # Lowercase the text
        text = text.lower()
        # Tokenize the text
        words = word_tokenize(text)
        # Filter for English words
        english_words = [word for word in words if wordnet.synsets(word)]
        # Remove stopwords
        stop_words = stopwords.words('english')
        english_words = [word for word in english_words if word not in stop_words]
        return english_words
    
    # Input: list of comments
    # Output: dictionary of word counter
    def wordFrequency(self, comment_list):
        word_dict = {}
        for comment in comment_list:
            word_list = self.clean_text(comment)
            for word in word_list:
                if word not in word_dict:
                    word_dict[word] = 1
                else:
                    word_dict[word] += 1
        return word_dict
    
if __name__ == '__main__':
    nlp = NLPTechniques()
    cf = CommentFinder()
    list_of_comments = cf.comment_finder("https://www.youtube.com/watch?v=YUVf0AFkn1Y")
    freq = nlp.wordFrequency(list_of_comments)
    sorted_freq = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
    for k, v in sorted_freq.items():
        print(k, ":", v)
