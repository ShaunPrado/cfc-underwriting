import requests
import requests_cache
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Scraper:
    """A scraper class to scrape and analyze a website's privacy policy and external resources."""

    session = None

    def __init__(self, base_url):
        """Initialize the scraper with the base URL of the website."""
        self.base_url = base_url
        if not Scraper.session:
            Scraper.session = requests_cache.CachedSession('base_url_cache', expire_after=3600)
    
    def get_soup_from_url(self, url):
        """Retrieve the HTML content of the given URL and return a BeautifulSoup object."""
        try:
            response = Scraper.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        except (requests.exceptions.RequestException, ValueError) as e:
            print("Error retrieving URL: ", url)
            return None

    def find_external_resources(self, soup):
        """Find and return a list of external resources (only src, href) found in the given BeautifulSoup object. TODO: Extend for other tags e.g img, script, etc."""
        resources = []
        for tag in soup.find_all():
            if tag.has_attr("src"):
                src = tag["src"]
                abs_url = urljoin(self.base_url, src)
                if self.base_url not in abs_url:
                    resources.append(abs_url)
            if tag.has_attr("href"):
                href = tag["href"]
                if href.startswith(("http", "https")):
                    abs_url = urljoin(self.base_url, href)
                    if self.base_url not in abs_url:
                        resources.append(abs_url)

        return resources

    def find_privacy_policy_url(self, soup):
        """Find and return the privacy policy URL found in the given BeautifulSoup object."""
        privacy_policy_url = None
        for link in soup.find_all("a"):
            if "privacy policy" in link.get_text().lower():
                href = link["href"]
                abs_url = urljoin(self.base_url, href)
                if abs_url != self.base_url and abs_url.endswith("/privacy-policy/"):
                    privacy_policy_url = abs_url
                    break
        return privacy_policy_url

    def get_visible_text(self, soup):
        """Extract and return visible text content from the given BeautifulSoup object."""
        main_section = soup.find('main', class_='individual-content')

        if main_section:
            sections = main_section.find_all(["h2", "p"])
            section_texts = []

            for section in sections:
                section_text = section.get_text().replace('\n', ' ').lower()
                section_text = re.sub(r"(-?\d+)((\.(-?\d+))+)?", ' ', section_text)
                section_text = section_text.replace('\xa0', ' ')
                section_texts.append(section_text)

            combined_text = ' '.join(section_texts)
            words = combined_text.split()
            cleaned_words = [re.sub(r'[^a-zA-Z0-9]+', '', word) for word in words]

            return cleaned_words

        return []

    def scrape_privacy_policy_page(self, url):
        """Scrape the privacy policy page at the given URL and save the word frequency to a JSON file."""
        soup = self.get_soup_from_url(url)
        words = self.get_visible_text(soup)
        word_count = self.get_word_frequency(words)

        self.write_to_json_file(word_count, "word_frequency.json")

    def get_word_frequency(self, words):
        """Compute the frequency of words in the given list and return a dictionary of word frequencies."""
        word_count = {}
        for word in words:
            if word:
                if word not in word_count:
                    word_count[word] = 1
                else:
                    word_count[word] += 1
        return word_count

    def write_to_json_file(self, data, filename):
        """Write the given data to a JSON file with the specified filename."""
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    base_url = "https://www.cfcunderwriting.com"
    scraper = Scraper(base_url)
    try:
        soup = scraper.get_soup_from_url(base_url)

        resources = scraper.find_external_resources(soup)
        scraper.write_to_json_file(resources, "external_resources.json")

        privacy_policy_url = scraper.find_privacy_policy_url(soup)
        if privacy_policy_url:
            scraper.scrape_privacy_policy_page(privacy_policy_url)
        else:
            print("Unable to find Privacy Policy page URL.")
    except requests.exceptions.ConnectionError as e:
        print("Connection error: ", e)
    except requests.exceptions.Timeout as e:
        print("Timeout error: ", e)
    except requests.exceptions.RequestException as e:
        print("Error: ", e)