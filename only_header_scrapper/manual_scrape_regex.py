# manual_scrape_regex.py

import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QApplication
)
import sys

class ManualScrapeRegex(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Manual Single-Line Regex Scraper')

        # Basic layout
        layout = QVBoxLayout()

        # URL Input
        self.url_label = QLabel('Enter URL:')
        self.url_input = QTextEdit()
        self.url_input.setPlaceholderText('https://example.com')

        # Buttons
        self.scrape_button = QPushButton('Generate Regex')
        self.scrape_button.clicked.connect(self.regex_genrt)

        # Generated Regex Box
        self.regex_label = QLabel('Generated Regex:')
        self.regex_box = QTextEdit()
        self.regex_box.setReadOnly(True)

        # Add widgets to layout
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.scrape_button)
        layout.addWidget(self.regex_label)
        layout.addWidget(self.regex_box)

        self.setLayout(layout)

    def regex_genrt(self):
        url = self.url_input.toPlainText().strip()
        try:
            if not url:
                self.regex_box.setPlainText('URL cannot be empty.')
                return

            regex_pattern = self.regex_genrt_pattern(url)
            self.regex_box.setPlainText(regex_pattern)

        except Exception as e:
            self.regex_box.setPlainText(f'Error: {str(e)}')

    def regex_genrt_pattern(self, url):
        try:
            # Extract the domain and TLD from the URL
            domain_pattern = r'https?://(?:www\.)?([a-z0-9-]+)\.([a-z]{2,})(?:\.[a-z]{2})?'
            match = re.match(domain_pattern, url)

            if match:
                domain = match.group(1)
                tld = match.group(2)
                
                if tld == "com" and ".tr" in url:
                    # Handle .com.tr
                    regex_pattern = f"^https?://(?:[a-z0-9-]+\\.)?{re.escape(domain)}\\.com\\.tr/.*$"
                else:
                    # Handle .com and other TLDs
                    regex_pattern = f"^https?://(?:[a-z0-9-]+\\.)?{re.escape(domain)}\\.{re.escape(tld)}/.*$"

                return regex_pattern
            else:
                raise ValueError("Invalid URL format")

        except Exception as e:
            raise RuntimeError(f'Error: {str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ManualScrapeRegex()
    window.show()
    sys.exit(app.exec_())
