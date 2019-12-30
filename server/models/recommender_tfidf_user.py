#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pymysql
from rake_nltk import Rake
from random import randint
from models.utils import cleanHtml, concatenate_list



def getRecommendations(userData, corr):
    recommendations = []

    for i in userData['skills']:
        for j in corr:

            if i.strip() in j['programName'].strip():
                for k in j['similarities']:

                    if k[0] > 0:
                        if k[1] not in recommendations:
                            for l in corr:
                                if l['programName'] == k[1]:
                                    recommendations.append(dict({'id': int(l['id']),
                                                                 'courseName': k[1].capitalize(),
                                                                 'url': str('http://timesshiksha.com/enrol/index.php?id=' + str(l['id']))}))
                    else:
                        break

    return recommendations



    ##========= SAMPLE USERDATA ================
    # userData = {
    #     'skills': ['tally']
    # }


def getRecommendationsForUser(skills=None, serving=True):

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='times_shiksha2')

    df = pd.read_sql('SELECT * FROM mdl_course', con=connection)
    df = df.copy()[['id', 'fullname', 'summary']]

    summarylist = []
    for line in df['summary']:
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

    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(df['Key_words'])

    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    results = {}
    for idx, row in df.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], df['fullname'][i]) for i in similar_indices]
        results[row['fullname']] = {'id': row['id'], 'similarities': similar_items[1:]}

    corr = []
    for progName, details in results.items():
        corr.append({'id': details['id'], 'programName': progName, 'similarities': details['similarities']})


    if serving:
        pass
    else:
        skills = input("Enter skills seperated by comma: \n")

    userData = {
        'skills': list(pd.Series(skills.split(',')).apply(lambda x: x.strip()))
    }


    finalResults = getRecommendations(userData, corr)
    return finalResults

def main():
    print(getRecommendationsForUser(serving=False))

if __name__ == '__main__':
    main()




#
