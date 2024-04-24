from flask import Flask, jsonify
from os import getenv

import pandas as pd
from transformers import pipeline
import re

DEBUG = getenv("DEBUG", "False").lower() in ("true", "1", "t")
SECRET_KEY = getenv("SECRET_KEY", "secret-key")

app = Flask(__name__)
app.secret_key = SECRET_KEY


pd.set_option("display.max_colwidth", None)

df = pd.read_csv(
    "./mbti/training.1600000.processed.noemoticon.csv",
    encoding="latin-1",
)
df.columns = ["target", "ids", "date", "flag", "user", "text"]

# trim the dataset so that the 100 most frequent values in 4th column are there
f = df[df.iloc[:, 4].isin(df.iloc[:, 4].value_counts().index[:200])]
f.iloc[:, 4].value_counts()
# save the trimmed dataset as new dataframe with column names

data = f.loc[:, ["user", "text"]]
data.describe()


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, "", input_txt)
    return input_txt


data["text"] = data["text"].str.replace(r"[@#][\w]*", "", regex=True)
data["text"] = data["text"].str.replace(r"http[s]?://\S+", "", regex=True)

# get unique users
collection = {}
for user in data.user.unique():
    collection[user] = data[data.user == user].iloc[:, 1].tolist()

sentiment_pipeline = pipeline(
    model="cardiffnlp/twitter-roberta-base-sentiment-latest")
hate_pipeline = pipeline(
    "text-classification", model="facebook/roberta-hate-speech-dynabench-r4-target"
)
misogyny_pipeline = pipeline(
    "text-classification",
    model="NLP-LTU/bertweet-large-sexism-detector",
)


@app.route('/sentiment/<name>', methods=['GET'])
def calculate_score(name):
    input = collection[name]
    sentiment = sentiment_pipeline(input, return_all_scores=True)
    hate = hate_pipeline(input, return_all_scores=True)
    misogyny = misogyny_pipeline(input, return_all_scores=True)
    hate_df = pd.DataFrame(hate)
    sentiment_df = pd.DataFrame(sentiment)
    misogyny_df = pd.DataFrame(misogyny)
    for columns in sentiment_df.columns:
        sentiment_df[columns] = sentiment_df[columns].apply(
            lambda x: x["score"])
    sentiment_df.columns = ["negative", "neutral", "positive"]
    for columns in hate_df.columns:
        hate_df[columns] = hate_df[columns].apply(lambda x: x["score"])
    hate_df.columns = ["nohate", "hate"]
    for columns in misogyny_df.columns:
        misogyny_df[columns] = misogyny_df[columns].apply(lambda x: x["score"])
    misogyny_df.columns = ["nonmisogyny", "misogyny"]
    user_data = pd.concat(
        [
            data[data.user == name].reset_index(drop=True),
            sentiment_df,
            hate_df,
            misogyny_df,
        ],
        axis=1,
    )
    controversial = user_data.loc[
        (user_data.hate > 0.75)
        | (user_data.misogyny > 0.75)
        | (user_data.negative > 0.75)
    ].text.values.tolist()

    # final_Data = pd.concat([final_Data, user_data], axis=0)

    # final_Data.to_csv("final_data.csv", sep=",", index=False, encoding="utf-8")

    sums = user_data[
        [
            "positive",
            "neutral",
            "negative",
            "nohate",
            "hate",
            "nonmisogyny",
            "misogyny",
        ]
    ].sum(axis=0)

    user_data.to_csv("sentiment_data.csv", sep=",",
                     index=False, encoding="utf-8")
    # print(controversial)
    # print("type:", type(controversial))
    # print(type(sums / len(user_data)))
    # print(sums / len(user_data))
    return jsonify((sums / len(user_data)).to_dict(), controversial)

if __name__ == "__main__":
    app.run(debug=DEBUG, host="0.0.0.0", port=80)