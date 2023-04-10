import re
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class NLPTechniques:
    # Cleans the list of comments
    def clean_text_array(self, comment_list):
        clean_arr = []
        for comment in comment_list:
            clean_text = self.clean_text(comment)
            if len(clean_text) > 2:
                clean_arr.append(clean_text)
        return clean_arr
    
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
        #Lemmatize the words
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in words]
        # Filter for English words
        english_words = [word for word in lemmatized_tokens if wordnet.synsets(word)]
        # Remove stopwords
        stop_words = stopwords.words('english')
        english_words = [word for word in english_words if word not in stop_words]
        return english_words
    
    # Input: list of comments
    # Output: dictionary of word counter
    def word_frequency(self, comment_list):
        word_dict = {}
        for comment in comment_list:
            for word in comment:
                if word not in word_dict:
                    word_dict[word] = 1
                else:
                    word_dict[word] += 1
        return word_dict
        
    # Input: String of clean words
    # Output: Sentiment score
    def sentiment_analysis(self, words):
        sa = SentimentIntensityAnalyzer()
        score = sa.polarity_scores(words)
        return [score['neg'] * 100, score['neu'] * 100, score['pos'] * 100]
    
if __name__ == '__main__':
    nlp = NLPTechniques()
    a = nlp.sentiment_analysis("Hello! I hate people. I like puppies.")
    print(a)