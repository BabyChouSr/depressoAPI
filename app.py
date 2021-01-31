import nltk
nltk.download('stopwords')
nltk.download('punkt')
import uvicorn
from fastapi import FastAPI
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tensorflow.keras 
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing import sequence
import re
import string 
import numpy as np

app = FastAPI()
model = tensorflow.keras.models.load_model("modelGLOVE9655only100.h5")

@app.get('/')
def index():
    return "The depressoAPI is currently running!"

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
        tweet = re.sub(r'#*', '', tweet)
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
    return " ".join([str(x) for x in text])

# @app.post('/moodDetect')
# def predict_mood(data:str):
#     text = data
#     sid = SentimentIntensityAnalyzer()
#     mood = sid.polarity_scores(processData(text))['compound']
#     return {
#         'mood': mood
#     }

@app.get('/moodDetect/{text}')
async def predict_mood(text):
    text = text
    print(processData(text))
    sid = SentimentIntensityAnalyzer()
    mood = sid.polarity_scores(processData(text))['compound']
    return {
        'mood': mood
    }

@app.get('/depressionDetect/{text}')
async def predict_depression(text):
    maxlen = 75
    text = text
    text = processData(text)
    text_list = text.split(" ")
    strings = open("word_index2.txt").read()
    newtext = " ".join([w for w in text_list if(w in strings)])
    newtext = np.array([newtext])
    print(newtext)
    t = Tokenizer()
    t.fit_on_texts(newtext)
    newX = t.texts_to_sequences(newtext)
    newX = pad_sequences(newX, maxlen = maxlen)
    classification = (model.predict(newX) >= 0.5).astype("int")
    print(model.predict(newX))
    if classification == 1:
        return {
            'classification' : "depressed"
        }
    return  {
        'classification' : "normal"
    }


if __name__ == '__main__':
    uvicorn.run( app, host='127.0.0.1', port=8000, debug = True)

