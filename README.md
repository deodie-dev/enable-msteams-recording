# MS Teams Recording Automation

This project ensures that Microsoft Teams meeting recordings are automatically enabled for client advisory calls. It works in conjunction with the AI Meeting Notes Automation project to ensure all meetings are properly recorded for later processing. The script is manually run by company administrators using business advisers' credentials.

## Tech Stack

- **Microsoft Graph API** – Retrieves meetings from Outlook calendar
- **Selenium WebDriver** – Automates browser interaction for enabling recording settings
- **Python** – Primary programming language for automation logic
- **Azure AD** – Authentication for Microsoft Graph API access

## Project Structure

```plaintext
.
├── main.py                          # Main entry point for the automation
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
├── README.md                        # Project documentation
└── app/
    ├── settings.py                  # Configuration settings (environment variables)
    ├── automation/
    │   ├── login.py                 # Microsoft login automation
    │   └── selenium_driver.py       # Selenium WebDriver setup
    ├── graph/
    │   ├── auth.py                  # Graph API authentication
    │   ├── client.py                # Graph API client wrapper
    │   └── calendar_service.py      # Outlook calendar operations
    ├── teams/
    │   ├── recording_services.py    # Recording settings automation
    │   └── url_builder.py           # Teams meeting URL construction
    ├── config/
    │   └── restricted_meetings.json # List of meetings to skip
    └── utils/
        ├── date_utils.py            # Date range utilities
        └── meeting_utils.py         # Meeting ID extraction utilities
```

### Key Components

- **`main.py`** - Orchestrates the entire workflow: authenticates with Graph API, retrieves meetings, filters them, and automates recording setup via browser automation
- **`app/automation/`** - Handles Selenium WebDriver creation and Microsoft login automation
- **`app/graph/`** - Manages Graph API authentication and Outlook calendar operations
- **`app/teams/`** - Constructs Teams meeting URLs and automates recording settings via the Teams UI
- **`app/config/`** - Contains restricted meetings configuration (meetings to skip)
- **`app/utils/`** - Utility functions for date calculations and meeting ID extraction

## Workflow Overview

1. **Authentication**  
   Script authenticates with Microsoft Graph API using business adviser credentials to access calendar and meeting data.

2. **Meeting Retrieval**  
   Fetches upcoming meetings from Outlook calendar within a configurable date range (NO_OF_DAYS environment variable).

3. **Meeting Filtering**  
   Applies filters to identify target meetings:
   - Skips meetings matching patterns in `restricted_meetings.json`
   - Processes only meetings with categories: "Client - Retainer" or "Client - Diagnostic"
   - Extracts meeting IDs from Teams join URLs

4. **Browser Automation**  
   Uses Selenium WebDriver to:
   - Log in to Microsoft Teams through browser
   - Navigate to meeting options page for each qualifying meeting
   - Enable auto-recording checkbox if not already enabled
   - Save the changes

## Setup Instructions

1. Create a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Configure environment variables and restricted meetings (see Configuration section below)

4. Ensure ChromeDriver is installed and accessible (Selenium will auto-download if needed)

## Configuration

### Environment Variables
Create a `.env` file in the project root with the following variables:
```plaintext
GRAPH_API_URL=https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
TENANT_ID=your_tenant_id
NO_OF_DAYS=7
```

### Restricted Meetings
Edit `app/config/restricted_meetings.json` to specify meetings to skip. Example:
```json
[
  {
    "subject": "restricted meeting",
    "email": "email@companyemail.co"
  },
  {
    "subject": "board review",
    "email": "ceo@companyemail.co"
  }
]
```
Meetings matching any subject or organizer email in this list will be skipped.

## Usage

Run the script with the business adviser's email and password:

```powershell
python main.py <EMAIL> <PASSWORD>
```

**Example:**
```powershell
python main.py adviser@company.com MySecurePassword123
```

The script will:
1. Authenticate with Microsoft Graph API
2. Retrieve meetings from the next N days (based on NO_OF_DAYS)
3. Filter meetings based on categories and restrictions
4. Launch a browser and log into Teams
5. Enable auto-recording for each qualifying meeting
6. Close the browser

**Note:** The browser automation is visible and interactive. Do not close the browser window while the script is running.

## Related Projects

This project works in conjunction with the [AI Meeting Notes Automation](https://github.com/deodie-dev/azure-func-app-aimeetingnotes) system:
- This script (`main.py`) ensures meetings are recorded
- The AI Meeting Notes system then processes these recordings to generate summaries

## Security Considerations

- Credentials are stored securely in `.env` file (not committed to repository)
- Script runs with minimum required permissions
- Manual execution ensures controlled access to meeting modifications
- Uses business adviser credentials for appropriate access level

## Troubleshooting

Common issues and solutions:

1. **Authentication errors:**
   - Verify CLIENT_ID, CLIENT_SECRET, and TENANT_ID in `.env` file
   - Ensure the application is registered in Azure AD with appropriate permissions
   - Check that credentials have access to the Graph API

2. **Meeting access issues:**
   - Confirm the adviser account is the organizer or has required permissions
   - Verify meetings have Teams online meeting links (joinURL)
   - Check that meetings are categorized correctly ("Client - Retainer" or "Client - Diagnostic")

3. **Selenium/Browser automation errors:**
   - Ensure Selenium and ChromeDriver are compatible versions
   - Verify the email and password are correct
   - Check for Microsoft MFA/2FA requirements (may need additional setup)
   - Try running with a fresh Chrome profile (no saved passwords/cookies)

4. **Module import errors:**
   - Verify all Python dependencies are installed: `pip install -r requirements.txt`
   - Ensure the working directory is the project root when running the script
   - Check that `app/` directory is in the Python path

## Support

For issues or assistance:
1. Check the Troubleshooting section above
2. Review Microsoft Graph API documentation: https://docs.microsoft.com/graph
3. Review Selenium documentation: https://www.selenium.dev/documentation/
4. Contact the Author

## Author

Built by Deodie Picson as part of a productivity and efficiency automation initiative. For inquiries or support, please contact deodie.dev@gmail.com.
