import glob
import os
import logging as log

from gtts import gTTS
from random import randint
from Config_and_Log import logs


module_directory = os.path.dirname(__file__)
logs.initialize_logger("tts")


def google_tts(text, lang, filename):
    log.debug("inside google_tts function.")
    
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(module_directory + "/" + filename)
        return filename
    
    except Exception as e:
        log.error("Error in google_tts. Error message: %s", e)
        return None


def guj_tts(text, filename):
    log.debug("inside guj_tts function.")

    try:
        # command on terminal.
        os.system("flite -voice " + module_directory + "/cmu_indic_axb_gu.flitevox '" + text + "' -o " +
                  module_directory + "/" + filename)
        return filename
    
    except Exception as e:
        log.error("Error in guj_tts. Error message: %s", e)
        return None


def tts_controller(text, lang):
    log.debug("inside tts_controller function.")

    # remove all files inside raw folder.
    try:
        files = glob.glob(module_directory + "/*.mp3")
        for f in files:
            os.remove(f)
    except Exception as e:
        log.error("Error while removing speech files. Error message: %s", e)

    # file name with random int append to it.
    filename = "speech_" + str(randint(0, 1000)) + ".mp3"

    if lang == "gu":
        return guj_tts(text, filename)
    
    elif lang == "en":
        return google_tts(text, "en-us", filename)

    else:
        return google_tts(text, lang, filename)
