import json
import requests
import pandas as pd
import csv
import pymongo
from pymongo import MongoClient

'''
Names (computing id): Hannah Lee (hsl8xrv), Joanne Lee (jl7yyb), Sammy Park (scp9cqg)
Date: 12/15/2022
Link: https://github.com/joanneslee/ds2002/tree/main/DS-2002-Final-Project
'''

'''
Reading in CSV datas as a pandas dataframe
    Only the Best Movies Netflix.csv and Best Shows Netflix.csv were used as the NUMBER_OF_VOTES and DURATION
    columns were missing from the other two csvs provided in the Kaggle website.
    
    Additionally, the raw_credits.csv and raw_titles.csv files weren't utilized as our questions didn't pertain to
    the information inside. 

https://www.kaggle.com/datasets/thedevastator/the-ultimate-netflix-tv-shows-and-movies-dataset?select=Best+Movies+Netflix.csv
'''
df1 = pd.read_csv('Best Movies Netflix.csv')
df2 = pd.read_csv('Best Shows Netflix.csv')

''' 
Concatenate the Best Movies and Best Shows dataframes into one pandas dataframe
'''
df3 = pd.concat([df1, df2])
# print("Number of records: ", len(df3), "\n",
#       "Number of columns: ", len(df3.columns))
# header = list(df3.columns.values)
# print(header)

'''
Delete columns "index", "NUMBER_OF_VOTES", and "NUMBER_OF_SEASONS" from concatenated dataframe to extract 
only 6 key variable columns
    The index column is not needed for the chatbot and the number of votes as well as the number of seasons
    were taken out to not allow the user to ask questions about votes and seasons for movies and shows. 
'''
df3 = df3.drop(['NUMBER_OF_VOTES', 'NUMBER_OF_SEASONS'], axis = 1)
# print("Number of records: ", len(df3), "\n",
#       "Number of columns: ", len(df3.columns))
# header = list(df3.columns.values)
# print(header)

movies = ["movie"] * 387
shows = ["show"] * 246
Movie_Show = movies + shows
df3['Movie_Show'] = Movie_Show

'''
Creating a new MongoDB and loading the data into it
'''
host_name = "localhost"
port = "27017"


conn_str = {
    "local" : f"mongodb://{host_name}:{port}/",
}

client = pymongo.MongoClient(conn_str["local"])

print(f"Local Connection String: {conn_str['local']}")

db_name = "netflix_database"
db = client[db_name]

# dataframe to documents
data_docs = df3.to_dict('records')
# print(data_docs)

# collection named films
films = db.films
film_id = films.insert_many(data_docs).inserted_ids
#print("Document ID: ", film_id)
print("Databases: ", client.list_database_names())
print("Collections: ", db.list_collection_names())

