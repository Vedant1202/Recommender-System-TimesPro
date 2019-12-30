#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from rake_nltk import Rake
from random import randint
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pymysql
from models.utils import cleanHtml, concatenate_list




#  defining the function that takes in movie title
# as input and returns the top 10 recommended movies
def get_recommendation(title, indices, cosine_sim, df):
    # initializing the empty list of recommendations
    recommendations = []
    target = False

    # gettin the index
    for i in indices:
        if title in i:
            target = i

    if target:
        idx = indices[indices == target].index[0]
        recommendations.append(dict({'id': int(df['id'][target]),
                                     'courseName': target.capitalize(),
                                     'url': str('http://timesshiksha.com/enrol/index.php?id=' + str(df['id'][target]))}))
    else:
        idx = randint(0, len(indices))

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

    # getting the indexes of the 10 most similar movies
    top_10_indexes = list(score_series.iloc[1:11].index)

    # populating the list with the titles of the best 10 matching movies

    for i in top_10_indexes:
        recommendations.append(dict({'id': int(df['id'][list(df.index)[i]]),
                                    'courseName': list(df.index)[i].capitalize(),
                                    'url': str('http://timesshiksha.com/enrol/index.php?id=' + str(df['id'][list(df.index)[i]]))}))

    return recommendations




def getRecommendationsForSearch(query=None, serving=True):

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='times_shiksha2')

    df = pd.read_sql('SELECT * FROM mdl_course', con=connection)

    df = df.copy()[['id', 'fullname', 'summary']]
    summarylist = []
    for line in df['summary']:
        line = cleanHtml(line)
        line = line.replace('\n','').replace('\r','').replace('\t','').lower()
        summarylist.append(line)

    df['summary'] = summarylist
    df['fullname'] = df['fullname'].str.lower()

    # initializing the new column
    df['Key_words'] = ""

    for index, row in df.iterrows():
        plot = str(row['summary'])

        # instantiating Rake, by default it uses english stopwords from NLTK
        # and discards all puntuation characters as well
        r = Rake()

        # extracting the words by passing the text
        r.extract_keywords_from_text(plot)

        # getting the dictionary whith key words as keys and their scores as values
        key_words_dict_scores = r.get_word_degrees()

        # assigning the key words to the new column for the corresponding movie
        row['Key_words'] = concatenate_list(list(key_words_dict_scores.keys()))
        df['Key_words'][index] = row['Key_words'].strip()

    # dropping the Plot column
    df.drop(columns = ['summary'], inplace = True)

    df.set_index(['fullname'], inplace=True)

    # instantiating and generating the count matrix
    count = CountVectorizer()
    count_matrix = count.fit_transform(df['Key_words'])

    # generating the cosine similarity matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    # creating a Series for the movie titles so they are associated to an ordered numerical
    # list I will use in the function to match the indexes
    indices = pd.Series(df.index)
    descs = pd.Series(df['Key_words'])


    if serving:
        pass
    else:
        query = input("Enter search keyword: \n")

    finalResults = get_recommendation(query, indices, cosine_sim, df)
    return finalResults


def main():
    print(getRecommendationsForSearch(serving=False))

if __name__ == '__main__':
    main()




#
