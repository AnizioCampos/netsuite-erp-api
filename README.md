
## Financial Data Management System Overview

This project automates the fetching, organizing, and updating of invoice and expense data from an API to Google Sheets, streamlining financial data management for businesses. It utilizes Python functions for date handling, security measures like timestamp generation and nonce creation, and employs OAuth for secure API requests to NetSuite's cloud-based business management software.

### Key Features

- **Invoice Data Management**: Automates the retrieval of detailed invoice data including ID, client information, dates, services, and payment status. Organizes this data in a pandas DataFrame for analysis and record-keeping.

- **Expense Data Management**: Handles expense data fetching, including details like transaction ID, issuance and payment dates, and financial specifics. Data is organized into a pandas DataFrame designed for tracking expenses efficiently.

### Integration with Google Sheets

Both invoice and expense data are written to separate sheets in a Google Sheets document using the `gspread` library. This integration facilitates:

1. **Data Conversion and Updating**: Converts pandas DataFrames into formats compatible with Google Sheets and updates sheets ("receita" for revenue/invoice data and "despesas" for expenses) with the latest information.

2. **Streamlined Financial Tracking**: Offers a consolidated view for easy tracking and analysis of financial transactions without manual data entry.

### Technical Stack

- **Python Libraries**: Utilizes `requests` for web requests, `pandas` for data manipulation, and `gspread` for managing Google Sheets.
- **Secure Authentication**: Leverages OAuth for authenticated API requests, ensuring data integrity and security.

### Conclusion

This system enhances financial data handling efficiency, leveraging Python's capabilities alongside secure and automated processes for managing financial transactions in Google Sheets.

---
