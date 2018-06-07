import httplib2
import os
import oauth2client
import base64
import logging as log

from oauth2client import client, tools
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
from Config_and_Log import logs, config


module_directory = os.path.dirname(__file__)
logs.initialize_logger("mail")


def get_credentials():
    log.debug("Inside get_credentials function.")

    scopes = str(config.email['scope'])
    client_secret_file = module_directory + '/client_secret.json'
    application_file = 'GMail APP'

    credential_path = module_directory + '/credentials.json'
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secret_file, scopes)
        flow.user_agent = application_file
        credentials = tools.run_flow(flow, store)
        log.debug('Storing credentials to ' + credential_path)

    return credentials


def send_mail(to, subject, message):
    log.debug("Inside send_mail function.")
    try:
        sender = str(config.email['id'])
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = to
        msg.attach(MIMEText(message, 'html'))

        raw = base64.urlsafe_b64encode(msg.as_bytes())
        raw = raw.decode()
        raw = {'raw': raw}

        user_id = "me"

        message = (service.users().messages().send(userId=user_id, body=raw).execute())
        log.debug('Message Id: %s' % message['id'])
        return message

    except errors.HttpError as error:
        log.error('Error in send_mail. An error occurred: %s' % error)
        return None
