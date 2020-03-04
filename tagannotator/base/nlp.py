import numpy as np
import scipy
import os
from django.conf import settings
from sklearn.neighbors import NearestCentroid
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import normalize
import wordninja

embedding_dict = {}
clf = None

contexts = ['activity', 'emotion', 'event', 'location', 'mood', 'object', 'time'] 
stop_words = []

def initialize():
    global embedding_dict, clf, contexts

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

    # with open('./tagannotator/glove.twitter.27B.25d.txt', encoding='utf-8') as f:
        stop_words = f.read().splitlines() # https://www.lextek.com/manuals/onix/stopwords1.html

    context_words = {}

    for c in contexts:
        # with open(os.path.join(settings.BASE_DIR, 'glove.twitter.27B.25d.txt'), encoding='utf-8') as f:
        with open(os.path.join(settings.BASE_DIR, '%s.txt' % c), encoding='utf-8') as f:
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
    # context_words['activity'] = activity
    # context_words['event'] = event
    # context_words['emotion'] = emotion
    # context_words['location'] = location
    # context_words['objects'] = objects
    # context_words['time'] = time
    # context_words['mood'] = mood

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

        return (contexts, normalized_distances.transpose())
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
            return (contexts, None)
        else:

            normalized_distances = scipy.stats.zscore(summed_distances)

            return (contexts, normalized_distances.transpose())

# initialize()
# print(predict('tokyo'))
# print(predict('birthday'))
# print(predict('happybirthday'))
# print(predict('school'))
# print(predict('winter'))
# print(predict('shopping'))

# # clf.predict([embedding_dict['tokyo']])
# # print(p)