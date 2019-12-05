#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from rake_nltk import Rake
from random import randint
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def concatenate_list(list):
    result= ''
    for element in list:
        result += ' ' + str(element)
    return result

#  defining the function that takes in movie title
# as input and returns the top 10 recommended movies
def get_recommendation(title, indices, cosine_sim):

    # initializing the empty list of recommendations
    recommendations = []
    target = False

    # gettin the index
    for i in indices:
        if title in i:
            target = i

    if target:
        idx = indices[indices == target].index[0]
        recommendations.append(target)
    else:
        idx = randint(0, len(indices))

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

    # getting the indexes of the 10 most similar movies
    top_10_indexes = list(score_series.iloc[1:11].index)

    # populating the list with the titles of the best 10 matching movies

    for i in top_10_indexes:
        recommendations.append(list(df3.index)[i])

    return recommendations


# In[190]:


def main(query=None, serving=True):

    df_main = pd.read_csv('./Program list.csv')
    df = df_main.copy()

    # initializing the new column
    df['Key_words'] = ""

    for index, row in df.iterrows():
        plot = str(row['Program Info'])

        # instantiating Rake, by default it uses english stopwords from NLTK
        # and discards all puntuation characters as well
        r = Rake()

        # extracting the words by passing the text
        r.extract_keywords_from_text(plot)

        # getting the dictionary whith key words as keys and their scores as values
        key_words_dict_scores = r.get_word_degrees()

        # assigning the key words to the new column for the corresponding movie
        row['Key_words'] = concatenate_list(list(key_words_dict_scores.keys()))

    # dropping the Plot column
    df.drop(columns = ['Program Info'], inplace = True)
    df.drop(columns = ['Timing'], inplace = True)

    df['desc'] = df[['Dept/Domain', 'Key_words']].apply(lambda x: ''.join(x.map(str)).lower(), axis=1)
    df['Program Name'] = df['Program Name'].apply(lambda x: str(x).lower())

    df3 = df.copy().drop(['Dept/Domain', 'Key_words'], axis=1)
    df3.set_index(['Program Name'], inplace=True)

    # instantiating and generating the count matrix
    count = CountVectorizer()
    count_matrix = count.fit_transform(df3['desc'])

    # generating the cosine similarity matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    # creating a Series for the movie titles so they are associated to an ordered numerical
    # list I will use in the function to match the indexes
    indices = pd.Series(df3.index)
    # print(indices)
    descs = pd.Series(df3['desc'])

    if serving:
        pass
    else:
        query = input("Enter search keyword: \n")

    print(get_recommendation(query, indices, cosine_sim))




if __name__ == '__main__':
    main()




#
