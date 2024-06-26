import os.path
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1YaEu6NBajPpCsz7NJFvn4978s76eja_No4e5AcwJXoE"


def get_wsh(wsh_name: str):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None

    creds = Credentials.from_service_account_file('./google_sheets/service_account.json', scopes=SCOPES)

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # if os.path.exists("./google_sheets/token.json"):
    #     creds = Credentials.from_authorized_user_file("./google_sheets/token.json", SCOPES)
    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             "./google_sheets/credentials.json", SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open("./google_sheets/token.json", "w") as token:
    #         token.write(creds.to_json())

    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API to fetch the last row and column
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=wsh_name).execute()
    values = result.get("values", [])

    if not values:
        print("No data found.")
        return

    len_columns = len(values[0])
    for v in values[1:]:
        count_not_columns = len_columns - len(v)
        if count_not_columns > 0:
            for i in range(0, count_not_columns):
                v.append('')

    return values


def refresh_token():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("./google_sheets/token.json"):
        creds = Credentials.from_authorized_user_file("./google_sheets/token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        with open("./google_sheets/token.json", "w") as token:
            token.write(creds.to_json())
