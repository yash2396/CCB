import nltk
import tflearn
import random
import json
import pickle
import os
import numpy as np
import tensorflow as tf
import logging as log

from Config_and_Log import logs, config


module_directory = os.path.dirname(__file__)
logs.initialize_logger("bot")


# clean up a sentence with stemming and lower-case
def clean_up_sentence(sentence):
    lemma = nltk.WordNetLemmatizer()
    sentence_words = nltk.word_tokenize(sentence)

    # =============================Here Spell correction method is implement===========================================
    sentence_words = [lemma.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)  

    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s: 
                bag[i] = 1

    return np.array(bag)


def classify(sentence, model, data):
    error_threshold = 0.3
    words = data['words']
    classes = data['classes']

    results = model.predict([bow(sentence, words)])[0]
    prediction = results
    results = [[i, r] for i, r in enumerate(results) if r > error_threshold]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []

    for r in results:
        return_list.append((classes[r[0]], r[1]))
    
    return return_list, prediction


def response(sentence, model, data, previous_context, user_id='123'):
    context = {}
    
    if user_id not in context:
        context[user_id] = {}
    
    results, prediction = classify(sentence, model, data)

    # import chat-bot intents file
    with open(os.path.abspath(module_directory + '/DataSet/dataset.json')) as json_data:
        intents = json.load(json_data)

    while results:
        for i in intents['intents']:
            if i['tag'] == results[0][0]:
                if 'context' in i:
                    context[user_id]['context'] = i['context']

                if context[user_id]['context'] == '':
                    context[user_id]['context'] = previous_context

                if context[user_id]['context'] == 'General' and previous_context == '':
                    context[user_id]['context'] = ''
                    general_message = config.response['no_context']
                    full_response = {'message': general_message, 'context': context[user_id]['context'],
                                     'userID': user_id, 'prediction': prediction}
                    return full_response

                if context[user_id]['context'] == 'General':
                    context[user_id]['context'] = previous_context

                # a random response from the intent
                if i['responses']:
                    full_response = {'message': random.choice(i['responses']), 'context': context[user_id]['context'],
                                     'userID': user_id, 'prediction': prediction}
                    return full_response
    else:
        for i in intents['intents']:
            if i['tag'] == "Unknown":
                full_response = {'message': random.choice(i['responses']), 'context': previous_context,
                                 'userID': user_id, 'prediction': None}
                return full_response
        
        results.pop(0)


def model_load():
    tf.reset_default_graph()

    data = pickle.load(open(os.path.abspath(module_directory + "/bot_files/BB_training_data"), "rb"))
    train_x = data['train_x']
    train_y = data['train_y']

    # Network building
    # net = tflearn.input_data([None, len(train_x[0])])
    # net = tflearn.embedding(net, input_dim=10000, output_dim=128)
    # net = tflearn.lstm(net, 128, return_seq=True, dropout=0.6)
    # net = tflearn.lstm(net, 128, dropout=0.6)
    # net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
    # net = tflearn.regression(net, optimizer='adam', learning_rate=0.001, loss='categorical_crossentropy')

    # Build neural network structure
    net = tflearn.input_data(shape=[None, len(train_x[0])])
    net = tflearn.fully_connected(net, len(train_y[0]))
    net = tflearn.dropout(net, 0.8)
    net = tflearn.fully_connected(net, len(train_y[0]))
    net = tflearn.dropout(net, 0.8)
    net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
    net = tflearn.regression(net)

    # Define model
    model = tflearn.DNN(net)

    # load saved model
    model.load(os.path.abspath(module_directory + '/bot_files/BBmodel.tflearn'))

    return {'data': data, 'model': model}


model_data = model_load()


def bot(input_message, previous_context, user_id='123', show_details=False):
    log.debug("inside bot function.")

    try:
        full_response = response(input_message, model_data['model'], model_data['data'], previous_context, user_id)

        if show_details:
            print("INPUT: " + input_message + " : " + previous_context)
            print("OUTPUT: " + str(full_response))

            if full_response['prediction'] is not None:
                classes = model_data['data']['classes']
                for i, j in zip(classes, full_response['prediction']):
                    print(str(i) + " : " + str(j))

            print(full_response['userID'] + ":" + full_response['context'] + " : " + full_response['message'])

        if full_response['prediction'] is None:
            log.debug("Failed To predict. For message: " + input_message)

        return full_response

    except Exception as e:
        log.error("Error in bot response. Error message: %s", e)
        return None
