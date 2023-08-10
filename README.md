# Aruba Access Point User Management Script

This Python script is designed to manage user access on an Aruba Access Point using the Netmiko library. It can add, delete, and synchronize user accounts between a CSV data source and the access point.

## Features

- Connects to an Aruba Access Point using SSH and Netmiko.
- Reads user data from a CSV file for operations.
- Adds new users with passwords to the access point.
- Deletes users from the access point.
- Synchronizes user accounts by comparing the CSV data with access point users.

## Prerequisites

- Python 3.x
- Netmiko library (`pip install netmiko`)
- Pandas library (`pip install pandas`)

## Configuration

Before running the script, make sure to:

1. Modify the `Aruba_Ap` dictionary with the appropriate device credentials.
2. Specify the paths to your CSV files for `GustinfoDataPath` and `TempuserDataPath`.

## Usage

1. Clone or download this repository to your local machine.
2. Install the required libraries (if not already installed) using `pip`.
3. Open a terminal or command prompt and navigate to the repository's directory.
4. Run the script using the following command:

   ```bash
   python main.py


## Important Note
- The script uses the Netmiko library for SSH connections, so ensure you have SSH access enabled on your Aruba Access Point.
- Make sure the CSV data follows the correct format for username and last name.
- This script assumes that the access point configuration matches the expected commands for user management.
## License
This project is open-source and available under the MIT License.
