# copied from Stack Overflow and slightly edited: https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python

import os
import oauth2client
from oauth2client import client, tools, file
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
import httplib2
from MatchProfile import MatchProfile

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'Burrito Buddies Gmail Service'

# store credentials in '.credentials' directory in the script directory
def get_credentials():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    credential_dir = os.path.join(project_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-burritobuddies-email-send.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def send_message(sender, to, subject, msgHtml, msgPlain):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message1 = create_message(sender, to, subject, msgHtml, msgPlain)
    send_message_internal(service, "me", message1)

def send_message_internal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def create_message(sender, to, subject, msgHtml, msgPlain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msgPlain, 'plain'))
    #msg.attach(MIMEText(msgHtml, 'html'))
    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    return body

def send_results(profiles, sender):
    for profile in profiles:
        to = profile.get_email()
        subject = "Your Burrito Buddies"
        msg_html = ""
        msg_plain = "Your top 10 matches are:/n"
        for i, match in enumerate(profile.get_top_matches()):
            msg_plain += "\t%d: %s, %.1f%% match\n" % (i + 1, match[0], match[1] * 100)
        msg_plain += "\nThanks for participating!\n"
        send_message(sender, to, subject, msg_html, msg_plain)

def main():
    sender = "burrito-buddies@burrito-buddies.iam.gserviceaccount.com"


if __name__ == '__main__':
    main()
