from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from typing import List
import temo
import json

from models import Users
import os
from db import db
import json

router = APIRouter()
import json

import pandas as pd
from transformers import pipeline
import numpy as np
import re
from os import getenv
import json

from sklearn.model_selection import train_test_split
import re
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

from joblib import dump, load

from tqdm import tqdm
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet', download_dir='./datasets')
nltk.download('stopwords', download_dir='./datasets')
nltk.data.path.append('./datasets')

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


class Lemmatizer(object):
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def __call__(self, sentence):
        return [self.lemmatizer.lemmatize(word) for word in sentence.split() if len(word) > 2]


class utils:
    def convertToBinary(ls):
        output = []
        for i in ls:
            temp_list = list(bin(i).replace("0b", ""))
            for j in range(len(temp_list)):
                temp_list[j] = int(temp_list[j])
            temp_list = [0]*(4 - len(temp_list)) + temp_list
            output.append(temp_list)
        return output

    def returnLabel(ls):
        output = ""
        if (ls[0] == 0):
            output += 'e'
        else:
            output += 'i'
        if (ls[1] == 0):
            output += 'n'
        else:
            output += 's'
        if (ls[2] == 0):
            output += 'f'
        else:
            output += 't'
        if (ls[3] == 0):
            output += 'j'
        else:
            output += 'p'
        return output

    def sampling(mode, df, col_name, class_names, count):
        dfs = []
        for class_name in class_names:
            if mode == 'under':
                df_class = df[df[col_name] == class_name]
                if len(df_class) > count:
                    df_class = df_class.sample(count, replace=False)
                dfs.append(df_class)
            elif mode == 'over':
                df_class = df[df[col_name] == class_name]
                if len(df_class) < count:
                    df_class = df_class.sample(count, replace=True)
                dfs.append(df_class)
        dfs = pd.concat(dfs)
        df_x = df[~df[col_name].isin(class_names)]
        return pd.concat([dfs, df_x])

    def get_train(train_data):

        X_train = np.vstack(np.array(train_data.posts))
        y_train = np.array(train_data.type)

        return X_train, y_train

    def clear_text_pred(df):
        data_length = []
        lemmatizer = WordNetLemmatizer()
        cleaned_text = []
        stop_words = set(stopwords.words('english'))  # Load stop words
        pers_types = ['INFP', 'INFJ', 'INTP', 'INTJ', 'ENTP', 'ENFP', 'ISTP',
                      'ISFP', 'ENTJ', 'ISTJ', 'ENFJ', 'ISFJ', 'ESTP', 'ESFP', 'ESFJ', 'ESTJ']
        pers_types = [p.lower() for p in pers_types]

        print("Cleaning The Dataset")
        for sentence in tqdm(df):

            sentence = sentence.lower()

            sentence = re.sub(
                'https?://[^\s<>"]+|www\.[^\s<>"]+', ' ', sentence)

            sentence = re.sub('[^0-9a-z]', ' ', sentence)

            sentence = " ".join([word for word in sentence.split(
            ) if word not in stop_words])  # Remove stop words
            # print(len(sentence))

            for p in pers_types:
                sentence = re.sub(p, '', sentence)
            # print(len(sentence))

            sentence = lemmatizer.lemmatize(sentence)  # Lemmatize words

            # Split data, measure length of new filtered data
            data_length.append(len(sentence.split()))

            cleaned_text.append(sentence)

        return cleaned_text, data_length

    def clear_text(df):
        data_length = []
        lemmatizer = WordNetLemmatizer()
        cleaned_text = []
        stop_words = set(stopwords.words('english'))  # Load stop words
        pers_types = ['INFP', 'INFJ', 'INTP', 'INTJ', 'ENTP', 'ENFP', 'ISTP',
                      'ISFP', 'ENTJ', 'ISTJ', 'ENFJ', 'ISFJ', 'ESTP', 'ESFP', 'ESFJ', 'ESTJ']
        pers_types = [p.lower() for p in pers_types]

        print("Cleaning The Dataset")
        for sentence in tqdm(df.posts):

            sentence = sentence.lower()

            sentence = re.sub(
                'https?://[^\s<>"]+|www\.[^\s<>"]+', ' ', sentence)

            sentence = re.sub('[^0-9a-z]', ' ', sentence)

            sentence = " ".join([word for word in sentence.split(
            ) if word not in stop_words])  # Remove stop words
            # print(len(sentence))

            for p in pers_types:
                sentence = re.sub(p, '', sentence)
            # print(len(sentence))

            sentence = lemmatizer.lemmatize(sentence)  # Lemmatize words

            # Split data, measure length of new filtered data
            data_length.append(len(sentence.split()))

            cleaned_text.append(sentence)

        return cleaned_text, data_length

    def vectorize(df, vectorizer):
        df, length = utils.clear_text_pred(df)
        # Applying Tfidf Vectorization
        print("Applying Tfidf Vectorization")

        # Applying the vectorizer transform
        train_post = vectorizer.transform(df).toarray()
        return train_post

    def split(df, size):

        # Cleaning The Data
        df.posts, length = utils.clear_text(df)

        # Splitting into train & test
        print("Splitting into train & test")
        train_data, test_data = train_test_split(
            df, test_size=size, random_state=0, stratify=df.type)

        # Applying Tfidf Vectorization
        print("Applying Tfidf Vectorization")
        vectorizer = TfidfVectorizer(
            max_features=5000, stop_words='english', tokenizer=Lemmatizer())
        vectorizer.fit(train_data.posts)

        # Applying the vectorizer transform
        train_post = vectorizer.transform(train_data.posts).toarray()
        test_post = vectorizer.transform(test_data.posts).toarray()

        # Label Encoding the classes as 0,1,2,3......
        print("Label Encoding the classes")
        target_encoder = LabelEncoder()

        # Getting the final train and test
        print("Getting the final train and test")
        train_target = target_encoder.fit_transform(train_data.type)
        test_target = target_encoder.fit_transform(test_data.type)
        # print(target_encoder.classes_)
        return train_post, test_post, train_target, test_target, vectorizer

model = load('./mbti/mbti_model.joblib')
df = pd.read_csv('./mbti/mbti_1.csv', index_col=False)
df_clean = df
df_clean.posts, df_clean_length = utils.clear_text(df)
X_train2, X_test2, y_train2, y_test2, vectorizer = utils.split(df_clean, 0.2)
df = pd.read_csv(
    "./mbti/training.1600000.processed.noemoticon.csv",
    encoding='latin-1'
)
df.columns = ["target", "ids", "date", "flag", "user", "text"]

def mbti(name):
    # import os
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))
    wordnet.synsets("hello")

    f = df[df.iloc[:, 4].isin(df.iloc[:, 4].value_counts().index[:200])]

    data = f.loc[:, ["user", "text"]]

    data["text"] = data["text"].str.replace(r"[@#][\w]*", "", regex=True)
    data["text"] = data["text"].str.replace(r"http[s]?://\S+", "", regex=True)

    collection = {}
    for user in data.user.unique():
        collection[user] = data[data.user == user].iloc[:, 1].tolist()

    name_to_send = np.random.choice(data.user.unique())
    input = collection[name_to_send]
    input, _ = utils.clear_text_pred(input)
    input = utils.vectorize(input, vectorizer)
    y_predict = model.predict(input)
    y_predict = utils.convertToBinary(y_predict)
    y_predict = np.array(y_predict)
    count_1 = np.count_nonzero(y_predict, axis=0)
    count_0 = y_predict.shape[0] - count_1
    prob_1 = count_1/y_predict.shape[0]
    prob_0 = count_0/y_predict.shape[0]
    stacked = np.vstack((prob_0, prob_1))
    probability = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    probability.append(
                        [stacked[i][0]*stacked[j][1]*stacked[k][2]*stacked[l][3], [i, j, k, l]])
    probability.sort(reverse=True)
    out = [utils.returnLabel(probability[0][1]),
           utils.returnLabel(probability[1][1])]
    return out

def llama_call(mbti):
    promt = (
        "Give pros and cons for a job applicant with the personality type "
        + mbti
        + ". Dont refer to yourself or the promter. Also dont give an introduction or greeting."
    )
    system_promt = "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. Also, try to give responses which are impersonal, meaning try not to refer to yourself or the asker.If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."
    # output = replicate.run(
    #     "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    #     input={
    #         "prompt": promt,
    #         "max_new_tokens": 500,
    #         "system_promt": system_promt,
    #     },
    # )
    output = ["Hello World", "Bye World", "New World", "Old World"]
    # The meta/llama-2-70b-chat model can stream output as it's running.
    # The predict method returns an iterator, and you can iterate over that output.

    result = []
    for item in output:
        # https://replicate.com/meta/llama-2-70b-chat/versions/
        # 02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3/
        # api#output-schema
        result.append(item)
    result = "".join(result)
    return result



def calculate_score(name):
    name_to_send = np.random.choice(data.user.unique())
    input = collection[name_to_send]
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
    return user_data




@router.get("/")
async def root():
    return {"message": "Working!"}

@router.get("/new")
async def new():
    return RedirectResponse(url="/")

@router.post("/new")
async def new_user(user: Users = Body(...)):
    print("=====================================")
    print(user)
    user = jsonable_encoder(user)
    print("=====================================")
    print(user)
    result = db.users.insert_one(user)
    print("=====================================")
    print(result)
    print("=====================================")
    if result.inserted_id:
        return {"message": user.get("_id")}
    raise HTTPException(status_code=400, detail="Some Error occured while creating entry. Please check the data!")

@router.get("/user/{id}")
async def user(id: str):
    user = db.users.find_one({"_id": id})
    if not user:
        raise HTTPException(status_code=400, detail="Couldn't find any user with the given id")
    return jsonable_encoder(user)

# @router.get('/skills')
# def skills(linkedin_link: str):
#     os.system(f"python3 linkedin.py --profile_link={linkedin_link} > output.txt")
#     fp = open("output.txt", "r")
#     jobs = fp.read()
#     fp.close()
#     jobs_index = jobs.find("\n{")
#     jobs = jobs[jobs_index:]
#     cleaned_string = jobs.replace("\n", "").replace("'", "\"")
#     return jsonable_encoder(cleaned_string)

@router.get('/mbti')
def mbti2(twitter_username: str):
    return mbti(twitter_username)

@router.get("/sentiment")
def sentiment(twitter_username: str):
    print("here")
    return calculate_score(twitter_username)

@router.get("/llama1")
def llama(strig: str):
    return llama_call("mbit", strig)

@router.get("/llama2")
def llama2(array1: int, array2: int, array3: int, array4: int, array5: int):
    return llama_call("none", [array1, array2, array3, array4, array5])

@router.get("/report")
def report(twitter_username: str = "Dogbook"):
    twitter_username = "Dogbook"
    mbti1 = mbti(twitter_username)
    sentiment = calculate_score(twitter_username)
    llama_out = llama_call(mbti1[0])

    return llama_out