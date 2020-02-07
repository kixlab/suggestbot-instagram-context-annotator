import numpy as np
import os
from django.conf import settings
from sklearn.neighbors import KNeighborsClassifier

embedding_dict = {}
clf = None

contexts = ['activity', 'emotion', 'event', 'location', 'mood', 'objects', 'time'] 


def initialize():
    global embedding_dict, clf, contexts

    if clf is not None:
        return

    with open(os.path.join(settings.BASE_DIR, 'glove.twitter.27B.25d.txt'), encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vec = np.asarray(values[1:], 'float32')
            embedding_dict[word] = vec

    context_words = {}


    location = ['seoul', 'newcastle', 'porto', 'restaurant', 'kruger', 'purdue', 'bali', 'office', 'park', 'cafe', 'school', 'wework', 'supermarket']
    activity = ['sleeping', 'workout', 'driving', 'reading', 'shopping', 'party', 'swimming', 'golf', 'run', 'eating']
    emotion = ['happy', 'sad', 'angry', 'fear', 'love', 'hope', 'joy', 'worry', 'disgust', 'pity']
    event = ['anniversary', 'birthday', 'farewell', 'welcome', 'graduation', 'bridalshower', 'newyear', 'seminar', 'competition', 'wedding']
    objects = ['pizza', 'flower', 'sky', 'medal', 'bike', 'car', 'book', 'coffee', 'shoes', 'tree']
    time = ['spring', 'summer', 'fall', 'winter', 'morning', 'afternoon', 'evening', 'night', 'nightlife', 'vacation', 'holiday', 'weekend', 'weekdays']
    mood = ['cozy', 'calm', 'romantic', 'cheerful', 'energetic', 'mellow', 'peaceful', 'mysterious', 'serious']
    context_words['activity'] = activity
    context_words['event'] = event
    context_words['emotion'] = emotion
    context_words['location'] = location
    context_words['objects'] = objects
    context_words['time'] = time
    context_words['mood'] = mood

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
            
    clf = KNeighborsClassifier()

    clf.fit(X, y)

def predict(word):
    try:
        embedding = embedding_dict[word]
        return (contexts, clf.predict_proba([embedding]))
    except KeyError:
        return (contexts, None)