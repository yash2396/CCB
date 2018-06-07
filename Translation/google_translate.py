import logging as log
from Config_and_Log import logs
from googletrans import Translator

logs.initialize_logger("google_translate")


def google_translate(text, source=None, destination=None):
    log.debug("inside google_translate function.")

    try:
        translator = Translator()
        return translator.translate(text, src=source, dest=destination).text

    except Exception as e:
        log.error("Error while translating. Error message: %s", e)
        return None
