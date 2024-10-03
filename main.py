import os
import json
import datetime
import warnings
#Import Google API
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
#Import Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True) 
options.add_argument('--log-level=3') #reducere unødvendig logs
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--disable-search-engine-choice-screen")
service = Service()
service.log_path = os.devnull


options.add_argument("headless")
driver = webdriver.Chrome(options=options)
#Scope og credentials for GOOGLE API
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'client_secret.json'


def getTamigoShifts(username, password):
    shifts = []
    
    driver.get("https://app.tamigo.com/Shift/Pages/EmployeeShifts.aspx")

    driver.implicitly_wait(3)
    Username = driver.find_element(By.ID, "Username")
    Username.send_keys(username)

    Password = driver.find_element(By.ID, "Password")
    Password.send_keys(password)
    Password.send_keys(Keys.ENTER)

    Table = driver.find_element(By.XPATH, '//tbody')
    Rows = Table.find_elements(By.TAG_NAME, 'tr')

    for row in Rows:
        Cells = row.find_elements(By.TAG_NAME, 'td')
        #Save the data as a Python dictionary
        if len(Cells) > 0 and Cells[0].text.strip()=="": 
            assignment = {
                "week": Cells[2].text.strip(),
                "date": Cells[3].text.strip()[3:],
                "timing": Cells[4].text.strip()[:10],
                "hours": Cells[5].text.strip().replace(",","."),
            }

            shifts.append(assignment)
            print(f"Shift on {Cells[3].text.strip()} stripped.")
    #Convert the dictionary to .json format
    shifts_json = json.dumps(shifts, indent=4, ensure_ascii=False)
    print(shifts)
    return shifts

def initGoogleCalendar():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the token for later uses
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    service = build('calendar', 'v3', credentials=creds)
    print("Init Google")
    return service

def addShiftsToGoogleCalendar(service, shifts):
    for shift in shifts:
        # Parse date and timing
        shift_date = datetime.datetime.strptime(shift["date"], "%d-%m-%Y").date()  # Parse date
        start_time, end_time = shift["timing"].split("-")  # Parse timing

        start_datetime = datetime.datetime.combine(shift_date, datetime.datetime.strptime(start_time, "%H:%M").time())
        end_datetime = datetime.datetime.combine(shift_date, datetime.datetime.strptime(end_time, "%H:%M").time())

        # Convert to ISO format required by Google Calendar API
        event = {
            'summary': 'Work Shift',
            'description': f"Work shift of {shift['hours']} hours",
            'start': {
                'dateTime': start_datetime.isoformat(),
                'timeZone': 'Europe/Copenhagen',  # Adjust timezone as needed
            },
            'end': {
                'dateTime': end_datetime.isoformat(),
                'timeZone': 'Europe/Copenhagen',  # Adjust timezone as needed
            },
        }

        try:
            # Insert the event into the user's calendar
            event_result = service.events().insert(calendarId='primary', body=event).execute()
            print(f"Shift on {shift['date']} added to Google Calendar")
        except HttpError as error:
            print(f"An error occurred: {error}")
            continue


def deleteTamigoShifts(service):
    print("Deleting shifts.")
    # Check for "Shift" in title
    events_result = service.events().list(calendarId='primary', q="Shift").execute()
    events = events_result.get('items', [])

    if not events:
        print("No shifts found.")
        return

    # Check for every shift and delete them
    for event in events:
        print(f"Deleting shift: {event['summary']} on {event['start']['dateTime']}")
        service.events().delete(calendarId='primary', eventId=event['id']).execute()

    print("All shifts deleted.")


def main():
    #Username and password variables can be permenantly set
    username = input("Tamigo Username: ") 
    password = input("Tamigo Password:")
    shifts = getTamigoShifts(username, password)
    service = initGoogleCalendar()
    deleteTamigoShifts(service) #Delete all the shifts, so they don't overlap
    addShiftsToGoogleCalendar(service, shifts)

if __name__ == "__main__":
    main()
