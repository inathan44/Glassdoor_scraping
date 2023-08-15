# Job Search Automation with Python

This project is a Python script that automates the job search process using Selenium, BeautifulSoup, and openpyxl. It allows you to search for job postings on Glassdoor that match your specified keywords and store the results in a CSV and Excel file. Data can be used for sales prospecting, data analysis, or whatever your project needs the data for!

## Getting Started

### Prerequisites

- Python 3
- Selenium
- BeautifulSoup
- openpyxl

You can install the required Python packages using the following command:

```bash
pip install selenium beautifulsoup4 openpyxl
```

# Usage
1. Clone this repository to your local machine.
2. Open the main file (main.py).
3. Edit the KEYWORDS list by replacing <YOURKEYWORDHERE> with your desired keyword(s) in the main.py file:
```python
KEYWORDS = ["YOURKEYWORDHERE"]
```
4. Run the script and wait for the driver to scrape all of the job listings it finds (can take between 2 - 20+ minutes)
5. Excel file will created in folder of the repo with this data: Title, Company, Company Size, Industry, Revenue, URL, and Job Post Age (If data isn't found N/A will be shown)
