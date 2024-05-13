import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
import streamlit as st
import json 
import requests 
from PIL import Image
from io import BytesIO
from template import Template
import io 


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')

def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text.lower())

    # Remove stopwords and non-alphabetic characters, and lemmatize tokens
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]

    # Join tokens into a string
    preprocessed_text = ' '.join(tokens)

    return preprocessed_text

def calculate_cosine_similarity(text1, text2):
    # Preprocess texts
    preprocessed_text1 = preprocess_text(text1)
    preprocessed_text2 = preprocess_text(text2)

    # Calculate TF-IDF vectors
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([preprocessed_text1, preprocessed_text2])

    # Calculate cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return cosine_sim[0][0]

def calculate_sentiment_similarity(text1, text2):
    # Calculate sentiment scores for both texts
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score1 = analyzer.polarity_scores(text1)['compound']
    sentiment_score2 = analyzer.polarity_scores(text2)['compound']

    # Calculate absolute difference between sentiment scores
    sentiment_diff = abs(sentiment_score1 - sentiment_score2)

    # Scale difference to range [0, 1]
    sentiment_similarity = 1 - sentiment_diff

    return sentiment_similarity

def calculate_combined_similarity(text1, text2, alpha=0.5):
    # Calculate similarity scores using both TF-IDF cosine similarity and sentiment similarity
    tfidf_similarity = calculate_cosine_similarity(text1, text2)
    sentiment_similarity = calculate_sentiment_similarity(text1, text2)

    # Combine scores using a weighted average
    combined_similarity = alpha * tfidf_similarity + (1 - alpha) * sentiment_similarity

    return combined_similarity

#-----------------streamlit page
des=st.text_input("Describe your meme in a sentence:")
top_score=0
top_index1=0
top_index2=0
top_index3=0
top_index4=0
top_index5=0
time_count=0
with open('inter.json','r') as f:
    data=json.load(f)
for i in data:
    name=data[i]["name"]
    if calculate_combined_similarity(des, name) >top_score:
        top_score=calculate_combined_similarity(des, name)
        top_index5=top_index4
        top_index4=top_index3
        top_index3=top_index2
        top_index2=top_index1
        top_index1=i
        time_count+=1
    Template.template=[top_index1,top_index2,top_index3,top_index4,top_index5][:time_count]
try:
    print(Template.template)
    for i in Template.template:
        url=data[str(i)]["url"]
        if url:
            if requests.get(url).status_code==200:
                st.image(Image.open(BytesIO(requests.get(url).content)))
        if data[str(i)]["image"]:
            image_stream = io.BytesIO(data[str(i)]["image"].encode('latin1'))
            image=st.image(Image.open(image_stream))
            st.image(image, caption='', use_column_width=True)
except:
    pass
