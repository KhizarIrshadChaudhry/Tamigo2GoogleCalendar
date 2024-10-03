# Tamigo2GoogleCalendar

**Tamigo2GoogleCalendar** automates the process of retrieving work shifts from [Tamigo](https://www.tamigo.com) and syncing them to your Google Calendar. This tool helps you avoid manual entry by automatically scheduling your shifts directly into Google Calendar.

## What is Tamigo?

[Tamigo](https://www.tamigo.com) is a workforce management solution that allows businesses to schedule shifts, track attendance, and manage employee work hours.

## Features

- Fetch work shifts from Tamigo.
- Automatically add shifts to Google Calendar.
- Avoid overlapping shifts by deleting old ones before syncing.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/KhizarIrshadChaudhry/Tamigo2GoogleCalendar.git
cd TamigoShiftSync
```

### 2. Install Requirements

Make sure you have Python installed. Then, install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Set Up Google API Credentials

To allow the program to add events to your Google Calendar, you need a `client_secret.json` file for Google API authentication.

- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project.
- Enable the **Google Calendar API**.
- Create OAuth 2.0 credentials and download the `client_secret.json` file.
- Place the `client_secret.json` file in the root directory of this project.

For detailed instructions, follow the [Google Calendar API documentation](https://developers.google.com/calendar/quickstart/python).

### 4. Run the Program

You can now run the program to sync your shifts:

```bash
python main.py
```

The program will prompt you for your Tamigo username and password, then sync your shifts to Google Calendar.

## Issues and Support

If you encounter any issues or have questions while using TamigoShiftSync, feel free to contact me directly or create an issue in the [GitHub repository](https://github.com/yourusername/TamigoShiftSync/issues).

Your feedback is valuable and will help improve the project!

## License

This project is licensed under the MIT License.
```

Make sure to replace `yourusername` with your actual GitHub username in the links!
