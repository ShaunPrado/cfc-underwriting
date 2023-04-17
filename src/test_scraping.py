import unittest
import requests
from bs4 import BeautifulSoup
from collections import Counter
from scraping import Scraper

class TestScraper(unittest.TestCase):
    """Test cases for the Scraper class."""

    def setUp(self):
        """Set up the test environment with sample data and a Scraper instance."""
        self.base_url = "https://www.cfcunderwriting.com"
        self.scraper = Scraper(self.base_url)
        self.privacy_policy_url = "https://www.cfcunderwriting.com/en-gb/support/privacy-policy/"
        self.example_privacy_policy_html = """<html>
            <head></head>
            <body>
                <main class="individual-content">
                    <div>
                        <h2>Privacy Policy</h2>
                        <p>This is our privacy policy.</p>
                        <p>It contains some words</p>
                    </div>
                </main>
            </body>
        </html>"""

    def test_scrape_index_page(self):
        """Test if the index page can be scraped and returns a BeautifulSoup object."""
        request = requests.get(self.base_url)
        self.assertEqual(request.status_code, 200)
        soup = self.scraper.get_soup_from_url(self.base_url)
        self.assertIsInstance(soup, BeautifulSoup)

    def test_find_external_resources(self):
        """Test if the Scraper can find and return a list of external resources."""
        soup = self.scraper.get_soup_from_url(self.base_url)
        external_resources = self.scraper.find_external_resources(soup)
        self.assertIsInstance(external_resources, list)
        self.assertTrue(all(['/' in r for r in external_resources]))
        self.assertTrue(all([self.base_url not in r for r in external_resources]))

    def test_find_privacy_policy_url(self):
        """Test if the Scraper can find and return the privacy policy URL."""
        soup = self.scraper.get_soup_from_url(self.base_url)
        result = self.scraper.find_privacy_policy_url(soup)
        self.assertEqual(result, self.privacy_policy_url)

    def test_get_visible_text(self):
        """Test if the Scraper can extract and return visible text content."""
        soup = self.scraper.get_soup_from_url(self.privacy_policy_url)
        result = self.scraper.get_visible_text(soup)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_word_frequency(self):
        """Test if the Scraper can compute and return word frequencies."""
        words = self.scraper.get_visible_text(BeautifulSoup(self.example_privacy_policy_html, 'html.parser'))
        expected_words = ['privacy', 'policy', 'this', 'is', 'our', 'privacy', 'policy', 'it', 'contains', 'some', 'words']
        actual_word_frequency = self.scraper.get_word_frequency(words)
        expected_word_frequency = Counter(expected_words)
        self.assertEqual(actual_word_frequency, expected_word_frequency, "Word frequency count mismatch")
