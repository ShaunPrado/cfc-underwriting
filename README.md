# CFC Underwriting Web Scraper
This repository contains a simple web scraper designed to extract privacy policy information from www.cfcunderwriting.com. This take-home project is part of the interview process for CFC Underwriting.
## Features
* Scrape content from a given URL
* Identify and extract external resources
* Find the privacy policy URL
* Scrape the privacy policy page content
* Perform a case-insensitive word frequency count
* Save extracted data in JSON format
## Requirements
* Python 3.6 or higher
* beautifulsoup4 package
* requests package

To install the dependencies, run:

```
pip install -r requirements.txt
```
This will install the dependencies listed in the requirements.txt file.

To install the dependencies manually, run:

```
pip install beautifulsoup4 requests
```

## Usage
1. Clone the repository:

```
git clone git@github.com:ShaunPrado/cfc-underwriting.git
cd cfc-underwriting
```
2. Run the script:
```
cd src
python scraper.py
```
3. The results will be saved in the src folder as word_frequency.json and external_resources.json.

* external_resources.json: Contains a list of external resources found on the target website.
* word_frequency.json: Contains the word frequency count from the privacy policy page.

## Running tests
To run the tests located in test_scraping.py, follow these steps:

```
python -m unittest test_scraping.py
```
This will run all the tests located in the test_scraping.py file.
