import numpy as np
import scipy
import os
from django.conf import settings
from sklearn.neighbors import NearestCentroid
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import normalize
import wordninja
import json, math, statistics, random

embedding_dict = {}
clf = None

contexts = ['activity', 'emotion', 'event', 'location', 'mood', 'object', 'time'] 
stop_words = []

def initialize():
    global embedding_dict, clf, contexts, stop_words

    if clf is not None:
        return
    with open(os.path.join(settings.BASE_DIR, 'glove.twitter.27B.25d.txt'), encoding='utf-8') as f:

    # with open('./tagannotator/glove.twitter.27B.25d.txt', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vec = np.asarray(values[1:], 'float32')
            embedding_dict[word] = vec

    with open(os.path.join(settings.BASE_DIR, 'stopwords.txt'), encoding='utf-8') as f:

    # with open('./tagannotator/stopwords.txt', encoding='utf-8') as f:
        stop_words = f.read().splitlines() # https://www.lextek.com/manuals/onix/stopwords1.html

    context_words = {}

    for c in contexts:
        with open(os.path.join(settings.BASE_DIR, '%s.txt' % c), encoding='utf-8') as f:
        
        # with open('./tagannotator/%s.txt' % c, encoding='utf-8') as f:
            words = f.read().splitlines()
            safe_words = [w for w in words if w in embedding_dict]

            context_words[c] = safe_words
            

    # with open('./tagannotator/glove.twitter.27B.25d.txt', encoding='utf-8') as f:


    # location = ['seoul', 'newcastle', 'porto', 'restaurant', 'kruger', 'purdue', 'bali', 'office', 'park', 'cafe', 'school', 'wework', 'supermarket']
    # activity = ['sleeping', 'workout', 'driving', 'reading', 'shopping', 'party', 'swimming', 'golf', 'run', 'eating']
    # emotion = ['happy', 'sad', 'angry', 'fear', 'love', 'hope', 'joy', 'worry', 'disgust', 'pity']
    # event = ['anniversary', 'birthday', 'farewell', 'welcome', 'graduation', 'bridalshower', 'newyear', 'seminar', 'competition', 'wedding']
    # objects = ['pizza', 'flower', 'sky', 'medal', 'bike', 'car', 'book', 'coffee', 'shoes', 'tree']
    # time = ['spring', 'summer', 'fall', 'winter', 'morning', 'afternoon', 'evening', 'night', 'nightlife', 'vacation', 'holiday', 'weekend', 'weekdays']
    # mood = ['cozy', 'calm', 'romantic', 'cheerful', 'energetic', 'mellow', 'peaceful', 'mysterious', 'serious']
    # context_words['activity'] = ['sleeping', 'workout', 'driving', 'reading', 'shopping', 'party', 'swimming', 'golf', 'run', 'eating']
    # context_words['event'] = ['anniversary', 'birthday', 'farewell', 'welcome', 'graduation', 'bridalshower', 'newyear', 'seminar', 'competition', 'wedding']
    # context_words['emotion'] = ['happy', 'sad', 'angry', 'fear', 'love', 'hope', 'joy', 'worry', 'disgust', 'pity']
    # context_words['location'] = ['seoul', 'newcastle', 'porto', 'restaurant', 'kruger', 'purdue', 'bali', 'office', 'park', 'cafe', 'school', 'wework', 'supermarket']

    # context_words['object'] = ['pizza', 'flower', 'sky', 'medal', 'bike', 'car', 'book', 'coffee', 'shoes', 'tree']
    # context_words['time'] = ['spring', 'summer', 'fall', 'winter', 'morning', 'afternoon', 'evening', 'night', 'nightlife', 'vacation', 'holiday', 'weekend', 'weekdays']
    # context_words['mood'] = ['cozy', 'calm', 'romantic', 'cheerful', 'energetic', 'mellow', 'peaceful', 'mysterious', 'serious']

    num_contexts = 0
    for context in contexts:
        num_contexts += len(context_words[context])

    i = 0
    X = np.zeros((num_contexts, 25), dtype='float')
    y = []
    for context in contexts:
        for word in context_words[context]:
            X[i] = embedding_dict[word]
            y.append(context)
            i += 1
            
    clf = NearestCentroid()

    clf.fit(X, y)

def predict(w):
    word = w.lower().strip()
    centroids = clf.centroids_
    if word in embedding_dict:
        embedding = embedding_dict[word]

        distances = euclidean_distances(centroids, embedding.reshape(1, -1))
        normalized_distances = scipy.stats.zscore(distances)
        # rd = np.reciprocal(distances)
        # normalized_distances = normalize(rd, norm = 'l1', axis = 0 )
        return (clf.classes_, normalized_distances.transpose())
        # return normalized_distances.transpose()
    else:
        frags = wordninja.split(word)
        summed_distances = None
        for f in frags:
            if f not in embedding_dict:
                continue
            elif f in stop_words:
                continue
            embedding = embedding_dict[f]

            distances = euclidean_distances(centroids, embedding.reshape(1, -1))

            if summed_distances is None:
                summed_distances = distances
            else:
                summed_distances = np.add(summed_distances, distances)
        if summed_distances is None:
            return  (clf.classes_, None)
            # return None
        else:

            normalized_distances = scipy.stats.zscore(summed_distances)
            return  (clf.classes_, normalized_distances.transpose())
            # return normalized_distances.transpose()

def main():
    classes_order = [6, 1, 7, 3, 2, 5, 4]
    myTags = {} # pk: txt

    with open('./base-tags.json', 'r') as f:
        baseTags = json.load(f)
        for t in baseTags:
            txt = t['fields']['text']

            myTags[t['pk']] = txt

        myTagMappings = {}

    with open('./base-mappings.json', 'r') as f:
        baseMappings = json.load(f)

    for m in baseMappings:
        context = m['fields']['context']
        tag = m['fields']['tag']
        
        if tag in myTagMappings.keys():
            myTagMappings[tag]['contexts'].append(context)
        else:
            tagTxt = myTags[tag]
            myTagMappings[tag] = {'text': tagTxt, 'contexts': [context]}

    myRandomChoices = random.sample(myTagMappings.keys(), 1000)

    precision1 = 0
    precision2 = 0
    precision3 = 0
    recall1 = 0
    recall2 = 0
    recall3 = 0

    for c in myRandomChoices:
        myMapping = myTagMappings[c]
        prediction = predict(myMapping['text'])
        ctxCount = len(myMapping['contexts'])

        if prediction is None:
            continue
        else:
            argsort = np.argsort(prediction)[0]

            p = [classes_order[argsort[0]], classes_order[argsort[1]], classes_order[argsort[2]]]
            
            for c in myMapping['contexts']:
                if c == p[0]:
                    recall1 += 1/(ctxCount)
                if c in p[0:2]:
                    recall2 += 1 / (ctxCount)
                if c in p:
                    recall3 += 1 / (ctxCount)


            # print(myMapping['text'], myMapping['contexts'], prediction)

            if p[0] in myMapping['contexts']:
                precision1 += 1
                precision2 += (1/2)
                precision3 += (1/3)
            if p[1] in myMapping['contexts']:
                precision2 += (1/2)
                precision3 += (1/3)
            if p[2] in myMapping['contexts']:
                precision3 += (1/3)

    print(precision1, precision2, precision3)
    print(recall1, recall2, recall3)

# initialize()
# main()



# initialize()
# print(predict('tokyo'))
# print(predict('birthday'))
# print(predict('happybirthday'))
# print(predict('school'))
# print(predict('winter'))
# print(predict('shopping'))

# # clf.predict([embedding_dict['tokyo']])
# # print(p)