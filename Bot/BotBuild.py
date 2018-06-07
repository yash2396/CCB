import os

import tflearn
import random
import json
import pickle
import numpy as np
import tensorflow as tf

from nltk import WordNetLemmatizer, word_tokenize

module_directory = os.path.dirname(__file__)


class BotBuild:

    def __init__(self):

        words = []
        classes = []
        documents = []
        ignore_words = ['?']

        lemma = WordNetLemmatizer()

        with open(module_directory + '/DataSet/dataset.json') as json_data:
            intents = json.load(json_data)

        for intent in intents['intents']:
            for pattern in intent['patterns']:
                w = word_tokenize(pattern)
                words.extend(w)
                documents.append((w, intent['tag']))
                if intent['tag'] not in classes:
                    classes.append(intent['tag'])

        words = [lemma.lemmatize(w.lower()) for w in words if w not in ignore_words]
        words = sorted(list(set(words)))

        classes = sorted(list(set(classes)))

        print(len(documents), "documents")
        print(len(classes), "classes", classes)
        print(len(words), "unique stemmed words", words)

        training = []
        output_empty = [0] * len(classes)

        for doc in documents:
            bag = []
            pattern_words = doc[0]
            pattern_words = [lemma.lemmatize(word.lower()) for word in pattern_words]
            for w in words:
                bag.append(1) if w in pattern_words else bag.append(0)

            output_row = list(output_empty)
            output_row[classes.index(doc[1])] = 1

            training.append([bag, output_row])

        random.shuffle(training)
        training = np.array(training)

        train_x = list(training[:, 0])
        train_y = list(training[:, 1])

        test_x = list(training[:, 0])
        test_y = list(training[:, 1])

        tf.reset_default_graph()

        model = BotBuild.build_model(train_x, train_y, test_x, test_y)

        p = BotBuild.bow("hello", words, lemma)
        print(p)
        print(classes)
        print(model.predict([p]))

        pickle.dump({'words': words, 'classes': classes, 'train_x': train_x, 'train_y': train_y},
                    open(module_directory + "/bot_files/BB_training_data", "wb"))

    @staticmethod
    def build_model(train_x, train_y, test_x, test_y):
        # Network building
        # net = tflearn.input_data([None, len(train_x[0])])
        # net = tflearn.embedding(net, input_dim=10000, output_dim=128)
        # net = tflearn.lstm(net, 128, return_seq=True, dropout=0.6)
        # net = tflearn.lstm(net, 128, dropout=0.6)
        # net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
        # net = tflearn.regression(net, optimizer='adam', learning_rate=0.001, loss='categorical_crossentropy')

        # Build neural network
        net = tflearn.input_data(shape=[None, len(train_x[0])])
        net = tflearn.fully_connected(net, len(train_y[0]))
        net = tflearn.dropout(net, 0.8)
        net = tflearn.fully_connected(net, len(train_y[0]))
        net = tflearn.dropout(net, 0.8)
        net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
        net = tflearn.regression(net)

        # Training
        model = tflearn.DNN(net, tensorboard_dir= module_directory + '/bot_logs')
        # model.fit(train_x, train_y, n_epoch=1000, validation_set=(test_x, test_y), show_metric=True, batch_size=32)
        model.fit(train_x, train_y, n_epoch=1000, batch_size=32, show_metric=True)
        model.save(module_directory + '/bot_files/BBmodel.tflearn')

        return model

    @staticmethod
    def clean_up_sentence(sentence, lemma):
        sentence_words = word_tokenize(sentence)
        sentence_words = [lemma.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    @staticmethod
    def bow(sentence, words, lemma, show_details=False):
        sentence_words = BotBuild.clean_up_sentence(sentence, lemma)
        bag = [0]*len(words)
        for s in sentence_words:
            for i, w in enumerate(words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)

        return np.array(bag)


if __name__ == "__main__":
    bot = BotBuild()
