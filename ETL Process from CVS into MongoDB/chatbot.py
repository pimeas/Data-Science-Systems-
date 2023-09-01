
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('punkt')

from nltk import word_tokenize,sent_tokenize

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
#read more on the steamer https://towardsdatascience.com/stemming-lemmatization-what-ba782b7c0bd8
import numpy as np 
import tflearn
import tensorflow as tf
import random
import json
import pickle
import netflix_mongo
import pprint

with open("intents.json") as file:
    data = json.loads(file.read())

try:
    with open("data.pickle","rb") as f:
        words, labels, training, output = pickle.load(f)

except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            
        if intent["tag"] not in labels:
            labels.append(intent["tag"])


    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
               bag.append(1)
            else:
              bag.append(0)
    
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        
        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)
    
    with open("data.pickle","wb") as f:
        pickle.dump((words, labels, training, output), f)


net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return np.array(bag)



def chat():
    print("Ask questions about: ")
    print(" - Length of best Netflix movie 5 years ago")
    print(" - Top 2022 Netflix Movie")
    print(" - Release year of best Netflix movie")
    print(" - Genre of shortest 2015 Netflix movie")
    print(" - Production company that produced the worst 2022 Netflix movie")
    print(" - Genre of the top 2020 Netflix show")
    print(" - Production company that produced the top Netflix show")
    print(" - Worst 2021 Netflix show")
    print(" - Average length of episode for best 2022 Netflix show")
    print(" - Genre of worst 2021 Netflix show")
    print("(type quit to stop)")
    while True:
        inp = input("Question: ")
        if inp.lower() == "quit":
            break

        if inp.lower() == "help":
            print("Ask questions about: ")
            print(" - Length of best Netflix movie 5 years ago")
            print(" - Top 2022 Netflix Movie")
            print(" - Release year of best Netflix movie")
            print(" - Genre of shortest 2015 Netflix movie")
            print(" - Production company that produced the worst 2022 Netflix movie")
            print(" - Genre of the top 2020 Netflix show")
            print(" - Production company that produced the top Netflix show")
            print(" - Worst 2021 Netflix show")
            print(" - Average length of episode for best 2022 Netflix show")
            print(" - Genre of worst 2021 Netflix show")
            print("(type quit to stop)")

        result = model.predict([bag_of_words(inp, words)])[0]
        result_index = np.argmax(result)
        tag = labels[result_index]

        if result[result_index] > 0.7:
            if tag == "First":
                pprint.pprint(netflix_mongo.films.find({"RELEASE_YEAR" : 2018, "Movie_Show" : "movie"}, {"TITLE":1, "DURATION":1}).sort("SCORE",-1).limit(1)[0])
            elif tag == "Second":
                pprint.pprint(netflix_mongo.films.find({"RELEASE_YEAR" : 2022, "Movie_Show" : "movie"}, {"TITLE":1, "SCORE":1}).sort("SCORE",-1).limit(1)[0])
            elif tag == "Third":
                pprint.pprint(netflix_mongo.films.find({"Movie_Show" : "movie"}, {"TITLE":1, "RELEASE_YEAR":1, "SCORE":1}).sort("SCORE",-1).limit(1)[0])
            elif tag == "Fourth":
                pprint.pprint(netflix_mongo.films.find({"RELEASE_YEAR" : 2015, "Movie_Show" : "movie"}, {"TITLE":1, "DURATION":1, "MAIN_GENRE":1}).sort("DURATION",1).limit(1)[0])
            elif tag == "Fifth":
                pprint.pprint(netflix_mongo.films.find({"RELEASE_YEAR" : 2022, "Movie_Show" : "movie"}, {"TITLE":1,"SCORE":1, "MAIN_PRODUCTION":1}).sort("SCORE",1).limit(1)[0])
            elif tag == "Sixth":
                pprint.pprint(netflix_mongo.films.find({"RELEASE_YEAR" : 2020, "Movie_Show" : "show"}, {"TITLE":1, "SCORE":1, "MAIN_GENRE":1}).sort("SCORE",-1).limit(1)[0])
            elif tag == "Seventh":
                pprint.pprint(netflix_mongo.films.find({"Movie_Show" : "show"}, {"TITLE":1, "SCORE":1, "MAIN_PRODUCTION":1}).sort("SCORE",-1).limit(1)[0])
            elif tag == "Eighth":
                pprint.pprint(netflix_mongo.films.find({"RELEASE_YEAR" : 2021, "Movie_Show" : "show"}, {"TITLE":1, "SCORE":1}).sort("SCORE",1).limit(1)[0])
            elif tag == "Ninth":
                pprint.pprint(netflix_mongo.films.find({"RELEASE_YEAR" : 2022, "Movie_Show" : "show"}, {"TITLE":1, "SCORE":1, "DURATION":1}).sort("SCORE",-1).limit(1)[0])
            elif tag == "Tenth":
                pprint.pprint(netflix_mongo.films.find({"RELEASE_YEAR" : 2021, "Movie_Show" : "show"}, {"TITLE":1, "SCORE":1, "MAIN_GENRE":1}).sort("SCORE",1).limit(1)[0])
            else:
                print("Please ask a question from the 10 categories provided above.")
        else:
            print("Please ask a question from the 10 categories provided above.")
chat()