import logging as log
import os

from Config_and_Log import logs, config
from Face_Detection.face_detection import face_detection
from Bot.bot import bot
from Operations.common_operation import fix_language_code, read_data_set
from Operations.database_operation import replace_tag_data, total_response_update, get_total_responses, get_table_name
from Translation.google_translate import google_translate
from Speech.tts import tts_controller

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

module_directory = os.path.dirname(__file__)
logs.initialize_logger("main_controller")


class BrowserInstance:

    def __init__(self):
        global driver
        log.debug("Initialing Browser Instances.")

        chrome_options = Options()
        chrome_options.add_argument("--kiosk")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("user-data-dir=" + str(config.browser_config['user_data_dir']) + "bitbot")

        driver = webdriver.Chrome(module_directory + "/Config_and_Log/chromedriver", chrome_options=chrome_options)
        driver.get(str(config.browser_config['url']) + "bitbot")
        log.debug("Running Browser Instances.")

    @staticmethod
    def refresh_instance():
        log.debug("Refreshing browser page.")
        driver.refresh()


def bot_controller(input_message, user_id, selected_language, context, show_details, mysql):
    # Get the Language code.
    selected_language = fix_language_code(selected_language)

    # Translate to english.
    if selected_language != "en":
        input_message = google_translate(input_message, selected_language, "en")

        # If translation failed.
        if input_message is None:
            return "", 500

        if show_details:
            print("Translated to eng from " + str(selected_language) + " message: " + str(input_message))

    # Get the user's message response.
    full_response = bot(input_message, context, user_id, show_details)

    # if the bot response failed.
    if full_response is None:
        return "", 500

    # Update total_response count.
    total_response_update(mysql, full_response['context'])

    # Don't update the context if the current context is Administration.
    if full_response['context'] != "Administration":
        context = full_response['context']
        if show_details:
            print("Context is : " + full_response['context'])

    # Replace tags with database data.
    full_response['message'] = replace_tag_data(mysql, full_response)

    # Translate to User's language.
    if selected_language != "en":
        full_response['message'] = google_translate(full_response['message'], "en", selected_language)

        # If translation failed.
        if full_response['message'] is None:
            return "", 500

        if show_details:
            print("Translated to user message: " + full_response['message'])

    # TTS
    tts_ = tts_controller(full_response['message'], selected_language)

    res = {'message': full_response['message'], 'filename': tts_, 'context': context}
    return res


def dashboard_controller(mysql, role):
    log.debug("Inside dashboard_controller function.")

    try:
        res = {'res': None}
        department = []
        i = 0

        if str(role) == "Administration":
            roles = get_table_name(mysql)
        else:
            roles = [role]

        for role in roles:
            if role == "Manager":
                continue

            department.append({'role': {'department': role, 'responses': None, 'success_response': None,
                                        'total_responses': None}})
            all_responses = read_data_set(mysql, role)

            if all_responses is not None:
                department[i]['role']['responses'] = all_responses
                department[i]['role']['total_responses'] = str(len(all_responses))
                department[i]['role']['success_response'] = str(get_total_responses(mysql, role))
                res['res'] = department

            else:
                return None

            i += 1

        return res

    except Exception as e:
        log.error("Error in dashboard_controller. Error message: %s", e)
        return None


def main_controller():
    log.debug("Initialing main controller.")
    # Set up Chrome instances.
    browser_driver = BrowserInstance()

    # face detection.
    face_detection(browser_driver)


if __name__ == "__main__":
    main_controller()
