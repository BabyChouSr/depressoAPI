import nltk
nltk.download('stopwords')
nltk.download('punkt')
import uvicorn
from fastapi import FastAPI
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import re
import string 


app = FastAPI()

@app.get('/')
def index():
    return {'message': 'Hello, World'}

# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
@app.get('/{name}')
def get_name(name: str):
    return {"What's Up Depresso": f'{name}'}

def processData(text):
    def processTweet(tweet):
        tweet = re.sub(r'\&\w*;', '', tweet)
        tweet = re.sub('@[^\s]+','',tweet)
        tweet = re.sub(r'\$\w*', '', tweet)
        tweet = tweet.lower()
        tweet = re.sub(r'https?:\/\/.*\/\w*', '', tweet)
        tweet = re.sub(r'#\w*', '', tweet)
        tweet = re.sub(r'[' + string.punctuation.replace('@', '') + ']+', ' ', tweet)
        tweet = re.sub(r'\b\w{1,2}\b', '', tweet)
        tweet = re.sub(r'\s\s+', ' ', tweet)
        tweet = tweet.lstrip(' ') 
        tweet = re.sub('https', ' ', tweet)
        tweet = ''.join(c for c in tweet if c <= '\uFFFF') 
        return tweet

    stop_words = set(stopwords.words('english'))  

    text = processTweet(text)
    word_tokens = RegexpTokenizer(r'\w+').tokenize(text)
    text = [word for word in word_tokens if not word in stop_words]
    return " ".join(str(x) for x in text)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

