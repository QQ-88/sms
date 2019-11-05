from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']        


def get_agenda(chosen_time):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    # chosen_time = time()
    amend_time = 24 - int(chosen_time)

    now = datetime.datetime.utcnow()
    display_time = now.replace(hour=int(chosen_time))
    from_time = (display_time + (datetime.timedelta(hours=amend_time))).isoformat() + 'Z'
    to_time = (display_time + (datetime.timedelta(hours=(amend_time + 24)))).isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=from_time, 
                                        timeMax=to_time, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    agenda = ''
    if not events:
        return 'No upcoming events found'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        event = start[11:16] + ' - ' + event['summary']
        agenda += (f"{event} \n")
    return f"Your agenda for tomorrow:" + '\n' + agenda
