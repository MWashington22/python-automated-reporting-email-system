# Python Automated Reporting & Email Delivery System

A Python automation tool that processes sales data, generates business reports and visualizations, stores records in SQLite, and automatically delivers reports through Gmail.

## Features

- CSV data processing with Pandas
- SQLite database integration
- Automated sales calculations using SQL
- Total sales and top-selling product summaries
- Sales chart generation with Matplotlib
- Automated email delivery using Gmail SMTP
- Chart attachments included in email reports
- Environment variables for credential management
- Scheduled execution through Windows Task Scheduler

## Technologies

- Python
- Pandas
- SQLite
- SQL
- Matplotlib
- Gmail SMTP
- Windows Task Scheduler

## Project Structure

```text
AutoReportBot/
|-- main.py
|-- sales.csv
|-- requirements.txt
|-- README.md
|-- .gitignore
```

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project directory:

```bash
cd AutoReportBot
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Set the following environment variables:

- `GMAIL_ADDRESS` - Gmail account used to send reports.
- `GMAIL_APP_PASSWORD` - Gmail app password.
- `REPORT_RECIPIENT` - Optional recipient email address. Defaults to the sender account.

Never commit email credentials or passwords to the repository.

## Usage

Run the application:

```bash
python main.py
```

The application processes the sample sales data, updates the SQLite database, generates a sales chart and report, and emails the report with the chart attached.

## Example Output

- Total Sales: $158.85
- Top Product: Hair Gel

*Example results based on the included sample sales data.*

## Automation

The script can be configured to run automatically at scheduled intervals using Windows Task Scheduler.

## Author

Python Automation & Data Processing Portfolio Project