import json
import logging as log
import os

from Config_and_Log import logs
from Operations.database_operation import dashboard_get_tag_data

module_directory = os.path.dirname(__file__)
logs.initialize_logger("common_operation")


def fix_language_code(selected_language):
    log.debug("inside fix_language_code function.")
    selected_language = str(selected_language).split("-")
    selected_language = selected_language[0]

    return selected_language


def read_data_set(mysql, role):
    log.debug("Inside read_data_set function.")

    # import chat-bot intents file
    with open(os.path.abspath(module_directory + '/../Bot/DataSet/dataset.json')) as json_data:
        intents = json.load(json_data)

    all_responses = []
    for i in intents['intents']:

        if i['context'] == str(role):
            res = dashboard_get_tag_data(mysql, role, i['responses'][0], i['tag'])

            if res['tags'] is not None:
                all_responses.append(res)

    return all_responses
