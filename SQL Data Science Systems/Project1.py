# Github link: https://github.com/pimeas/Project-1.git
import json
import requests
import pandas as pd
import csv

# Description: The dataset is called Mobile phone rating with
# 8 columns for the phone model, price in USD, launch date (from August 31, 2013
# to December 31, 2021), camera rating, selfie rating, audio rating, display
# rating, and battery rating over time. The dataset was pulled from Dxomark's smartphones mobile rankings.
# The aim of this data processor is for the user to input the name of a phone model and gain information about
# its price, launch date, and rating of camera, audio, display, and battery life.

# 1) Reading in the csv data
data = pd.read_csv('mobile phone rating by dxo.csv')
# header = list(data.columns.values)
# print(header)

# 5) Number of rows and columns
print("Number of records: ", len(data), "\n",
      "Number of columns: ", len(data.columns))

# 3) Delete the column 'selfie' because the quality of a selfie may be
# dependent on the reviewer's photography skills
df = data.drop(['selfie'], axis = 1)
# header = list(df.columns.values)
# print(header)

# Gain user input and output a JSON file
try:
    # Retrieve name of phone model
    phone = input("Enter name of the phone model: ")

    # Find index of the phone model name
    name_index = df.index[df['model'] == phone].tolist()
    index = str(name_index)[1:-1]

    # Displaying price, launch, camera, audio, display, and battery
    price = df.loc[int(index), 'price']
    launch = df.loc[int(index), "launch"]
    camera = df.loc[int(index), "camera"]
    audio = df.loc[int(index), "audio"]
    display = df.loc[int(index), "display"]
    battery = df.loc[int(index), "battery"]

    print("Price in USD: ", price, "\n",
          "Launch date: ", launch, "\n",
          "Camera rating: ", camera, "out of 144.0", "\n",
          "Audio rating: ", audio, "out of 81.0", "\n",
          "Display rating: ", display, "out of 99.0", "\n",
          "Battery rating: ", battery, "out of 96.0", "\n",
          )

    model_information = {"Phone model": phone,
                         "Price in USD": price,
                         "Camera Rating out of 144.0": camera,
                         "Audio Rating out of 81.0": audio,
                         "Display Rating out of 99.0": display,
                         "Battery Life Rating out of 96.0": battery}

    # 4) Convert the new file locally to json format
    json_form = json.dumps(model_information)

    with open("phone_model_info.json", "w") as json_file:
        json_file.write(json_form)


except:
    print("The phone model cannot be found in the dataset and/or the name was misspelled.")
