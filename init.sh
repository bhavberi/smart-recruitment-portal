#!/usr/bin/env bash

# copy all `.env.example`s to `.env`s
find . -name ".*.example" -exec sh -c 'f="{}"; cp "$f" "$(echo $f | sed "s/.example//g")"' \;

# The dataset file
cd AI/mbti/mbti/
if [ ! -f "training.1600000.processed.noemoticon.csv" ]; then
    wget https://raw.githubusercontent.com/crwong/cs224u-project/master/data/sentiment/training.1600000.processed.noemoticon.csv
fi
if [ ! -f "mbti_1.csv" ]; then
    wget -O mbti_1.csv https://raw.githubusercontent.com/bhavberi/se-project-3/csv_data/mbti_1.csv?token=GHSAT0AAAAAACCIWJ4ZK2G5FA3BUV4PNJK4ZRJIYSA
fi

cd ../../sentiment/mbti/
cp ../../mbti/mbti/training.1600000.processed.noemoticon.csv .
cp ../../mbti/mbti/mbti_1.csv .

