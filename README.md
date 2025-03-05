# NSF Research Email Scraper

## Overview
This script scrapes research award data from the NSF (National Science Foundation) website using various scientific and technical keywords. It extracts principal investigator (PI) emails, names, funding programs, and awardee state codes, saving the data into a CSV file.

### Key Statistics
- **Total Emails Scraped:** 9.5 million
- **Unique Emails Extracted:** 67,000

## Features
- **Multi-threading:** Uses `ThreadPoolExecutor` to improve performance.
- **Keyword Expansion:** Generates up to 50,000 keyword variations to maximize data extraction.
- **Rate Limiting:** Implements delays to avoid overwhelming the server.
- **Incremental CSV Writing:** Saves results periodically to prevent data loss.
- **Logging:** Tracks progress and errors for debugging.

## Dependencies
Ensure you have Python 3 installed and the following dependencies:

```sh
pip install requests
```

## Usage
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/email-scraper.git
   cd email-scraper
   ```
2. Run the script:
   ```sh
   python scraper.py
   ```

## Script Breakdown

### 1. Keyword Generation
```python
def generate_keywords():
```
- Expands a base list of scientific and technical keywords by combining them with suffixes like "research," "study," and "innovation."
- Returns a list of **50,000** unique search keywords.

### 2. Fetching Award Data
```python
def fetch_award_data(keyword, results_per_page=25, filename="emails.csv"):
```
- Sends requests to the NSF API using search keywords.
- Extracts relevant award details, including **PI email, name, funding program, and award title.**
- Saves unique emails to avoid duplicates.
- Handles pagination and errors gracefully.

### 3. Saving to CSV
```python
def save_to_csv_incremental(data_list, filename="emails.csv"):
```
- Appends new data to an existing CSV file.
- Ensures headers are written only once.
- Saves in an incremental manner to avoid memory overload.

### 4. Multi-threaded Execution
```python
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_award_data, keywords))
```
- Uses 10 threads to fetch data in parallel, improving efficiency.
- Ensures that each keyword is processed independently.

## Output Format
The script stores extracted data in `emails.csv` with the following format:

| First Name | Middle Initial | Last Name | Email | Fund Program | State Code | Title |
|------------|---------------|-----------|-------|--------------|------------|-------|
| John       | A             | Doe       | john.doe@example.com | AI Research | CA | Deep Learning Study |
| Jane       | B             | Smith     | jane.smith@example.com | Climate Science | TX | Weather Modeling |

## Logging & Error Handling
- Logs all requests and errors for troubleshooting.
- Implements retries with exponential backoff in case of request failures.

## Future Improvements
- **Proxy Support:** To avoid rate-limiting issues.
- **Database Storage:** Instead of CSV, store data in a database for better querying.
- **Advanced Filtering:** Extract more metadata and filter results based on relevance.

## License
This project is licensed under the MIT License.

## Contributing
Feel free to submit pull requests or report issues!

## Contact
For questions, contact **your.email@example.com** or create an issue in this repository.

