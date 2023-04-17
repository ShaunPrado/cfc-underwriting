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
python3 scraper.py
```
3. The results will be saved in the src folder as word_frequency.json and external_resources.json.
external_resources.json contains an array, where each entry represents an external resource found on the website.

Here is an example of what the word_frequency.json file might look like:

```json
[
    "https://fonts.googleapis.com/css?family=Montserrat:300,400,500,600,700",
    "https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/css/bootstrap.min.css",
    "https://www.googletagmanager.com/ns.html?id=GTM-NGGN5FB"
]
```

word_frequency.json contains a dictionary of word frequencies found in the privacy policy page. The keys of the dictionary are the individual words, and the values are the frequency of occurrence of each word in the page.

Here is an example of what the word_frequency.json file might look like:

```json
{
    "our": 54,
    "approach": 1,
    "this": 9
}
```

## Running tests
To run the tests located in test_scraping.py, follow these steps:

```
python3 -m unittest test_scraping.py
```
This will run all the tests located in the test_scraping.py file.

## Potential improvements

* Increase test coverage. Use mock objects to test the scraper rather than the live site
* Discuss trade-offs between using Selenium (to handle dynamic JS content) vs BeautifulSoup.
* Add more error handling
* Use logging instead of printing
* Caching the parsed HTML to improve performance.
* Integrate with a CI/CD pipeline (e.g github actions)
* Add a Dockerfile to containerize the application
* Add a Makefile to simplify the build process
* Extend find_external_resources: Refactor the find_external_resources method to handle more than just the src and href attributes, and consider storing metadata about the resources.
* Generalize get_visible_text: Refactor the get_visible_text method to be more generic, rather than hardcoded for the specific website.
