# MS Teams Recording Automation

This project ensures that Microsoft Teams meeting recordings are automatically enabled for client advisory calls. It works in conjunction with the AI Meeting Notes Automation project to ensure all meetings are properly recorded for later processing. The script is manually run by company administrators using business advisers' credentials.

## Tech Stack

- **Microsoft Graph API** – Manages Teams meeting settings and recording configurations
- **Python** – Primary programming language for automation logic
- **Azure AD** – Authentication for Microsoft Graph API access

## Project Structure

```plaintext
.
├── auto_record.py          # Main script for managing Teams recording settings
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
```

### `auto_record.py`
- Authenticates with Microsoft Graph API using business adviser credentials
- Retrieves upcoming meetings from calendar
- Checks and enables recording settings for each meeting
- Logs operation results and any issues encountered

## Workflow Overview

1. **Authentication**  
   Script uses business adviser credentials to authenticate with Microsoft Graph API.

2. **Meeting Retrieval**  
   Fetches upcoming meetings from the calendar within a specified timeframe.

3. **Recording Configuration**  
   For each meeting:
   - Checks current recording settings
   - Enables recording if not already enabled
   - Verifies the change was successful

4. **Logging**  
   Records all operations and their results for audit purposes.

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

3. Configure environment variables:
   - Create a `.env` file with the following:
     ```plaintext
     CLIENT_ID=your_client_id
     CLIENT_SECRET=your_client_secret
     TENANT_ID=your_tenant_id
     USER_EMAIL=adviser_email@domain.com
     ```

## Usage

The script is designed to be run manually by administrators:

```powershell
python auto_record.py <EMAIL> <PASSWORD>
```

## Related Projects

This project works in conjunction with the [AI Meeting Notes Automation](https://github.com/deodie-dev/azure-func-app-aimeetingnotes) system:
- This script (`auto_record.py`) ensures meetings are recorded
- The AI Meeting Notes system then processes these recordings to generate summaries

## Security Considerations

- Credentials are stored securely in `.env` file (not committed to repository)
- Script runs with minimum required permissions
- Manual execution ensures controlled access to meeting modifications
- Uses business adviser credentials for appropriate access level

## Troubleshooting

Common issues and solutions:
1. Authentication errors:
   - Verify credentials in `.env` file
   - Ensure adviser account has appropriate permissions
   
2. Meeting access issues:
   - Confirm adviser is an organizer or has adequate permissions
   - Check if meeting was created in supported calendar

## Support

For issues or assistance:
1. Contact the Author
2. Reference the related AI Meeting Notes system documentation
3. Check Microsoft Graph API documentation for Teams recording settings

## Author

Built by Deodie Picson as part of a productivity and efficiency automation initiative. For inquiries or support, please contact deodie.dev@gmail.com.
