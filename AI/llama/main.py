from flask import Flask, jsonify, request
import replicate
import os


app = Flask(__name__)


@app.route('/llama/<test>', methods=['GET'])
def llama_call(test):
    if test == "mbit":
        mbit = request.args.get('mbit')
        promt = (
            "Give pros and cons for a job applicant with the personality type "
            + mbit
            + ". Dont refer to yourself or the promter. Also dont give an introduction or greeting."
        )
    else:
        promt = (
            "Give a report for a job applicant with the big 5 scores of"
            + request.args.get('score1')
            + ", "
            + request.args.get('score2')
            + ", "
            + request.args.get('score3')
            + ", "
            + request.args.get('score4')
            + ", "
            + request.args.get('score5')
            + ", "
            + " where max is 40. Make it specifically in regards of their hirability Dont refer to yourself or the promter. Also dont give an introduction or greeting."
        )
    system_promt = "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. Also, try to give responses which are impersonal, meaning try not to refer to yourself or the asker.If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."
    output = replicate.run(
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={
            "prompt": promt,
            "max_new_tokens": 500,
            "system_promt": system_promt,
        },
    )
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
