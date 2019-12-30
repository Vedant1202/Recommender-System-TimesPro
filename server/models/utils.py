import re
import mysql.connector
import string

def cleanHtml(sentence):
  cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
  cleantext = re.sub(cleanr, '',sentence)
  return cleantext.translate(str.maketrans('', '', string.punctuation))


def concatenate_list(list):
    result= ''
    for element in list:
        result += ' ' + str(element)
    return result










#
