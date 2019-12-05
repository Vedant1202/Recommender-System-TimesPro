{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "from rake_nltk import Rake"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 162,
   "metadata": {},
   "outputs": [],
   "source": [
    "from random import randint"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.metrics.pairwise import cosine_similarity\n",
    "from sklearn.feature_extraction.text import CountVectorizer"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 168,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_main = pd.read_csv('./Program list.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 169,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "df = df_main.copy()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 170,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Program Name</th>\n",
       "      <th>Dept/Domain</th>\n",
       "      <th>Timing</th>\n",
       "      <th>Program Info</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Big Data</td>\n",
       "      <td>Computer Science and Engineering Information T...</td>\n",
       "      <td>01:10</td>\n",
       "      <td>Big Data is also data but with a huge size. Bi...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Data Science</td>\n",
       "      <td>Computer Science and Engineering Information T...</td>\n",
       "      <td>02:30</td>\n",
       "      <td>Data science is a \"concept to unify statistics...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Extract Tranform Load</td>\n",
       "      <td>Computer Science and Engineering Information T...</td>\n",
       "      <td>05:15</td>\n",
       "      <td>In computing, extract, transform, load is the ...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Extract Load Tranform</td>\n",
       "      <td>Computer Science and Engineering Information T...</td>\n",
       "      <td>02:00</td>\n",
       "      <td>ELT is an alternative to extract, transform, l...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Accounting</td>\n",
       "      <td>Finance</td>\n",
       "      <td>09:00</td>\n",
       "      <td>Accounting is the process of recording financi...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "            Program Name                                        Dept/Domain  \\\n",
       "0               Big Data  Computer Science and Engineering Information T...   \n",
       "1           Data Science  Computer Science and Engineering Information T...   \n",
       "2  Extract Tranform Load  Computer Science and Engineering Information T...   \n",
       "3  Extract Load Tranform  Computer Science and Engineering Information T...   \n",
       "4             Accounting                                            Finance   \n",
       "\n",
       "  Timing                                       Program Info  \n",
       "0  01:10  Big Data is also data but with a huge size. Bi...  \n",
       "1  02:30  Data science is a \"concept to unify statistics...  \n",
       "2  05:15  In computing, extract, transform, load is the ...  \n",
       "3  02:00  ELT is an alternative to extract, transform, l...  \n",
       "4  09:00  Accounting is the process of recording financi...  "
      ]
     },
     "execution_count": 170,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 171,
   "metadata": {},
   "outputs": [],
   "source": [
    "def concatenate_list(list):\n",
    "    result= ''\n",
    "    for element in list:\n",
    "        result += ' ' + str(element)\n",
    "    return result"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 172,
   "metadata": {},
   "outputs": [],
   "source": [
    "# initializing the new column\n",
    "df['Key_words'] = \"\"\n",
    "\n",
    "for index, row in df.iterrows():\n",
    "#     print(row)\n",
    "#     print(index)\n",
    "    plot = str(row['Program Info'])\n",
    "    \n",
    "    # instantiating Rake, by default it uses english stopwords from NLTK\n",
    "    # and discards all puntuation characters as well\n",
    "    r = Rake()\n",
    "\n",
    "    # extracting the words by passing the text\n",
    "    r.extract_keywords_from_text(plot)\n",
    "\n",
    "    # getting the dictionary whith key words as keys and their scores as values\n",
    "    key_words_dict_scores = r.get_word_degrees()\n",
    "    \n",
    "    # assigning the key words to the new column for the corresponding movie\n",
    "    row['Key_words'] = concatenate_list(list(key_words_dict_scores.keys()))\n",
    "    \n",
    "# dropping the Plot column\n",
    "df.drop(columns = ['Program Info'], inplace = True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 173,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "' complex store describe yet growing exponentially term used collection huge size process large able traditional data management tools big time efficiently also short none'"
      ]
     },
     "execution_count": 173,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df['Key_words'][0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 174,
   "metadata": {},
   "outputs": [],
   "source": [
    "df.drop(columns = ['Timing'], inplace = True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 175,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Program Name</th>\n",
       "      <th>Dept/Domain</th>\n",
       "      <th>Key_words</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Big Data</td>\n",
       "      <td>Computer Science and Engineering Information T...</td>\n",
       "      <td>complex store describe yet growing exponentia...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Data Science</td>\n",
       "      <td>Computer Science and Engineering Information T...</td>\n",
       "      <td>unify statistics order concept employs techni...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Extract Tranform Load</td>\n",
       "      <td>Computer Science and Engineering Information T...</td>\n",
       "      <td>sources computing one destination system load...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Extract Load Tranform</td>\n",
       "      <td>Computer Science and Engineering Information T...</td>\n",
       "      <td>etl entry alternative data lake implementatio...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Accounting</td>\n",
       "      <td>Finance</td>\n",
       "      <td>reporting transactions recording financial pe...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "            Program Name                                        Dept/Domain  \\\n",
       "0               Big Data  Computer Science and Engineering Information T...   \n",
       "1           Data Science  Computer Science and Engineering Information T...   \n",
       "2  Extract Tranform Load  Computer Science and Engineering Information T...   \n",
       "3  Extract Load Tranform  Computer Science and Engineering Information T...   \n",
       "4             Accounting                                            Finance   \n",
       "\n",
       "                                           Key_words  \n",
       "0   complex store describe yet growing exponentia...  \n",
       "1   unify statistics order concept employs techni...  \n",
       "2   sources computing one destination system load...  \n",
       "3   etl entry alternative data lake implementatio...  \n",
       "4   reporting transactions recording financial pe...  "
      ]
     },
     "execution_count": 175,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 176,
   "metadata": {},
   "outputs": [],
   "source": [
    "df['desc'] = df[['Dept/Domain', 'Key_words']].apply(lambda x: ''.join(x.map(str)).lower(), axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 177,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Program Name</th>\n",
       "      <th>Dept/Domain</th>\n",
       "      <th>Key_words</th>\n",
       "      <th>desc</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Big Data</td>\n",
       "      <td>Computer Science and Engineering Information T...</td>\n",
       "      <td>complex store describe yet growing exponentia...</td>\n",
       "      <td>computer science and engineering information t...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Data Science</td>\n",
       "      <td>Computer Science and Engineering Information T...</td>\n",
       "      <td>unify statistics order concept employs techni...</td>\n",
       "      <td>computer science and engineering information t...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Extract Tranform Load</td>\n",
       "      <td>Computer Science and Engineering Information T...</td>\n",
       "      <td>sources computing one destination system load...</td>\n",
       "      <td>computer science and engineering information t...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Extract Load Tranform</td>\n",
       "      <td>Computer Science and Engineering Information T...</td>\n",
       "      <td>etl entry alternative data lake implementatio...</td>\n",
       "      <td>computer science and engineering information t...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Accounting</td>\n",
       "      <td>Finance</td>\n",
       "      <td>reporting transactions recording financial pe...</td>\n",
       "      <td>finance reporting transactions recording finan...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "            Program Name                                        Dept/Domain  \\\n",
       "0               Big Data  Computer Science and Engineering Information T...   \n",
       "1           Data Science  Computer Science and Engineering Information T...   \n",
       "2  Extract Tranform Load  Computer Science and Engineering Information T...   \n",
       "3  Extract Load Tranform  Computer Science and Engineering Information T...   \n",
       "4             Accounting                                            Finance   \n",
       "\n",
       "                                           Key_words  \\\n",
       "0   complex store describe yet growing exponentia...   \n",
       "1   unify statistics order concept employs techni...   \n",
       "2   sources computing one destination system load...   \n",
       "3   etl entry alternative data lake implementatio...   \n",
       "4   reporting transactions recording financial pe...   \n",
       "\n",
       "                                                desc  \n",
       "0  computer science and engineering information t...  \n",
       "1  computer science and engineering information t...  \n",
       "2  computer science and engineering information t...  \n",
       "3  computer science and engineering information t...  \n",
       "4  finance reporting transactions recording finan...  "
      ]
     },
     "execution_count": 177,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 178,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'computer science and engineering information technology all unify statistics order concept employs techniques many fields within context mathematics understand information science theories drawn related methods machine learning computer data analysis analyze actual phenomena'"
      ]
     },
     "execution_count": 178,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df['desc'][1]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 179,
   "metadata": {},
   "outputs": [],
   "source": [
    "df['Program Name'] = df['Program Name'].apply(lambda x: str(x).lower())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 180,
   "metadata": {},
   "outputs": [],
   "source": [
    "df3 = df.copy().drop(['Dept/Domain', 'Key_words'], axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 181,
   "metadata": {},
   "outputs": [],
   "source": [
    "# df2 = df.copy().drop(['Dept/Domain', 'Key_words'], axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 182,
   "metadata": {},
   "outputs": [],
   "source": [
    "df3.set_index(['Program Name'], inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 183,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>desc</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Program Name</th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>big data</th>\n",
       "      <td>computer science and engineering information t...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>data science</th>\n",
       "      <td>computer science and engineering information t...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>extract tranform load</th>\n",
       "      <td>computer science and engineering information t...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>extract load tranform</th>\n",
       "      <td>computer science and engineering information t...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>accounting</th>\n",
       "      <td>finance reporting transactions recording finan...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                                                    desc\n",
       "Program Name                                                            \n",
       "big data               computer science and engineering information t...\n",
       "data science           computer science and engineering information t...\n",
       "extract tranform load  computer science and engineering information t...\n",
       "extract load tranform  computer science and engineering information t...\n",
       "accounting             finance reporting transactions recording finan..."
      ]
     },
     "execution_count": 183,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df3.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 184,
   "metadata": {},
   "outputs": [],
   "source": [
    "# instantiating and generating the count matrix\n",
    "count = CountVectorizer()\n",
    "count_matrix = count.fit_transform(df3['desc'])\n",
    "\n",
    "# generating the cosine similarity matrix\n",
    "cosine_sim = cosine_similarity(count_matrix, count_matrix)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 185,
   "metadata": {},
   "outputs": [],
   "source": [
    "# creating a Series for the movie titles so they are associated to an ordered numerical\n",
    "# list I will use in the function to match the indexes\n",
    "indices = pd.Series(df3.index)\n",
    "# print(indices)\n",
    "descs = pd.Series(df3['desc'])\n",
    "\n",
    "#  defining the function that takes in movie title \n",
    "# as input and returns the top 10 recommended movies\n",
    "def get_recommendation(title, cosine_sim = cosine_sim):\n",
    "    \n",
    "    # initializing the empty list of recommendations\n",
    "    recommendations = []\n",
    "    target = False\n",
    "    \n",
    "    # gettin the index\n",
    "    for i in indices:\n",
    "        if title in i:\n",
    "            target = i\n",
    "    \n",
    "    if target:\n",
    "        idx = indices[indices == target].index[0]\n",
    "        recommendations.append(target)\n",
    "    else:\n",
    "        idx = randint(0, len(indices))\n",
    "        \n",
    "    # creating a Series with the similarity scores in descending order\n",
    "    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)\n",
    "\n",
    "    # getting the indexes of the 10 most similar movies\n",
    "    top_10_indexes = list(score_series.iloc[1:11].index)\n",
    "    \n",
    "    # populating the list with the titles of the best 10 matching movies\n",
    "    \n",
    "    for i in top_10_indexes:\n",
    "        recommendations.append(list(df3.index)[i])\n",
    "        \n",
    "    return recommendations"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 190,
   "metadata": {},
   "outputs": [],
   "source": [
    "def main():\n",
    "    query = input()\n",
    "    print(get_recommendation(query))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 192,
   "metadata": {
    "scrolled": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "data\n",
      "['data structure', 'array', 'natural language processing', 'cloud computing', 'data science', 'operating system', 'algorithm', 'c programming language', 'pascal programming language', 'extract load tranform', 'big data']\n"
     ]
    }
   ],
   "source": [
    "main()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
