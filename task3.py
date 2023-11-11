from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
import os
import pickle
import matplotlib.pyplot as plt
from collections import Counter


def plot_bar_graph(valuedict):
    """
    Plots a bar graph
    :param valuedict: Dictionary frequency of items
    """
    fig, ax = plt.subplots()
    x = valuedict.keys()
    y = valuedict.values()
    bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:purple', 'tab:pink']

    ax.bar(x, y, color=bar_colors)

    ax.set_title('House Type')
    plt.show()
    

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID of the spreadsheet.
SPREADSHEET_ID = '1HSJarrTevcqeSblr61I_jv1Z14PAAK0yjdSwhFYhyMA'


def main():
    credentials = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    elif not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())
    try:
        # Call the Sheets API
        service = build('sheets', 'v4', credentials=credentials)
        sheets = service.spreadsheets()
        result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range='train!Q2:Q1461').execute()
        
        # Storing the retrived values
        values = result.get('values', [])
        values = [i[0] for i in values]
        valuedict = Counter(values)
        
        plot_bar_graph(valuedict)
    except HttpError as error:
        print(error)
        
if __name__ == '__main__':
    main()