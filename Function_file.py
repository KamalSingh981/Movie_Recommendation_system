import ast
from nltk.stem.porter import PorterStemmer


def convert(obj):
    l = []
    for i in ast.literal_eval(obj):
        l.append(i['name'])
    return l


def convert3(obj):
    l = []
    counter = 0
    for i in ast.literal_eval(obj):
        if(counter != 3):
            l.append(i['name'])
            counter += 1
        else:
            break
    return l


def fetch_director(obj):
    l = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            l.append(i['name'])
            break
    return l


def stem(text):
    y = []
    ps = PorterStemmer()
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)