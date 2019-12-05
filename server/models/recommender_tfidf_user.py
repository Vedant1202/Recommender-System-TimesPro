#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def getRecommendations(userData, corr):
    userCorr = corr[userData['aoi']]
    recommendations = userData['skills']

    for i in userCorr:
        if i['programName'] in userData['skills']:

            for j in i['similarities']:

                if j[0] > 0:
                    recommendations.append(j[1])
                else:
                    break

    return recommendations

##========= SAMPLE USERDATA ================
# userData = {
#     'aoi': 'finance',
#     'skills': ['tally']
# }


def getRecommendationsForUser(aoi=None, skills=None, serving=True):

    df_main = pd.read_csv('./data/Program list.csv')
    df = df_main.copy()

    df = df.apply(lambda x: x.astype(str).str.lower())


    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(df['Program Info'])

    df.drop(columns = ['Timing'], inplace = True)


    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    results = {}
    for idx, row in df.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], df['Program Name'][i]) for i in similar_indices]
        results[row['Program Name']] = {'dept/domain': row['Dept/Domain'], 'similarities': similar_items[1:]}


    domains = df['Dept/Domain'].unique()


    corr = {}
    for dom in domains:
        mat = []
        for progName, details in results.items():

            if details['dept/domain'] == dom:
                mat.append({'programName': progName, 'similarities': details['similarities']})

        corr[dom] = mat


    if serving:
        pass
    else:
        aoi = input("Enter Area of Interest / Dept / Domain: \n")
        skills = input("Enter skills seperated by comma: \n")

    userData = {
        'aoi': aoi.strip(),
        'skills': list(pd.Series(skills.split(',')).apply(lambda x: x.strip()))
    }

    finalResults = getRecommendations(userData, corr)
    print(finalResults)
    if serving:
        return finalResults
