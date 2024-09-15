import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QTabWidget
)
from PyQt5.QtCore import Qt
from scrape_links import scrape_links  # Import the function from scrape_links.py
from scrape_regex import test_regex  # Updated: Import the test_regex function instead
from manual_scrape_regex import ManualScrapeRegex  # Import the class
from bulk_regex_generator import generate_bulk_regex_patterns  # Import the function

class LinkScraperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Link Scraper Application')
        self.setGeometry(50, 50, 600, 600)  # Set initial size
        self.tabs = QTabWidget()
        
        # Initialize tabs
        self.link_scraper_tab = QWidget()
        self.regex_scraper_tab = QWidget()
        self.manual_regex_scraper_tab = QWidget()
        self.bulk_regex_scraper_tab = QWidget()  # Add a tab for bulk regex generation
        
        self.tabs.addTab(self.link_scraper_tab, "Link Scraper")
        self.tabs.addTab(self.regex_scraper_tab, "Regex Tester")  # Updated: Changed tab name
        self.tabs.addTab(self.manual_regex_scraper_tab, "Manual Regex Scraper")
        self.tabs.addTab(self.bulk_regex_scraper_tab, "Bulk Regex Scraper")  # Add tab for bulk regex scraper
        
        # Set up the UI for each tab
        self.init_link_scraper_ui()
        self.init_regex_scraper_ui()  # Updated: Renamed method for the regex tester
        self.init_manual_regex_scraper_ui()
        self.init_bulk_regex_scraper_ui()  # Initialize bulk regex scraper UI
        
        # Set up main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        
        # Dark-White mode
        self.dark_mode = False
        self.load_style()

    def load_style(self):
        style_file = 'darkstyle.qss' if self.dark_mode else 'whitestyle.qss'
        style_file_path = self.resource_path(style_file)
        try:
            with open(style_file_path, 'r') as file:
                style = file.read()
            self.setStyleSheet(style)
        except FileNotFoundError:
            print(f"Style file '{style_file}' not found.")

    def resource_path(self, relative_path):
        """ Get the absolute path to the resource file, handling PyInstaller packaging. """
        if getattr(sys, 'frozen', False):
            # Running in a bundled executable
            base_path = sys._MEIPASS
        else:
            # Running in a normal Python environment
            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)

    def toggle_mode(self):
        self.dark_mode = not self.dark_mode
        self.load_style()
        self.update_mode_button_text()
        
    def update_mode_button_text(self):
        if self.dark_mode:
            self.mode_button.setText('Switch to Light Mode')
        else:
            self.mode_button.setText('Switch to Dark Mode')

    def init_link_scraper_ui(self):
        layout = QVBoxLayout()

        # URL Input
        self.url_label = QLabel('Enter URL:')
        self.url_input = QTextEdit()
        self.url_input.setPlaceholderText('https://example.com')
        
        # Filename Input
        self.filename_label = QLabel('Enter filename:')
        self.filename_input = QTextEdit()
        self.filename_input.setPlaceholderText('examplename (without .txt)')
        
        # Buttons
        self.scrape_button = QPushButton('Scrape Links')
        self.scrape_button.clicked.connect(self.scrape_links)
        self.mode_button = QPushButton('Switch to Dark Mode')
        self.mode_button.clicked.connect(self.toggle_mode)
        self.clear_button = QPushButton('Clear All')
        self.clear_button.clicked.connect(self.clear_all)

        # Captured Links Box
        self.captured_links_label = QLabel('Captured Links:')
        self.captured_links_box = QTextEdit()
        self.captured_links_box.setReadOnly(True)
        
        # Add widgets to layout
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.filename_label)
        layout.addWidget(self.filename_input)
        layout.addWidget(self.scrape_button)
        layout.addWidget(self.mode_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.captured_links_label)
        layout.addWidget(self.captured_links_box)
        
        self.link_scraper_tab.setLayout(layout)
    
    def init_regex_scraper_ui(self):
        layout = QVBoxLayout()

        # Regex Pattern Input
        self.regex_pattern_label = QLabel('Enter Regex Pattern:')
        self.regex_pattern_input = QTextEdit()
        self.regex_pattern_input.setPlaceholderText('Enter your regex pattern here...')
        
        # Test String Input
        self.regex_test_string_label = QLabel('Enter Test String:')
        self.regex_test_string_input = QTextEdit()
        self.regex_test_string_input.setPlaceholderText('Enter the string to test against...')
        
        # Buttons
        self.regex_test_button = QPushButton('Test Regex')
        self.regex_test_button.clicked.connect(self.test_regex)  # Updated: Connected to the new test function
        self.regex_clear_button = QPushButton('Clear All')
        self.regex_clear_button.clicked.connect(self.clear_all)

        # Matched Results Box
        self.regex_results_label = QLabel('Matches Found:')
        self.regex_results_box = QTextEdit()
        self.regex_results_box.setReadOnly(True)
        
        # Add widgets to layout
        layout.addWidget(self.regex_pattern_label)
        layout.addWidget(self.regex_pattern_input)
        layout.addWidget(self.regex_test_string_label)
        layout.addWidget(self.regex_test_string_input)
        layout.addWidget(self.regex_test_button)
        layout.addWidget(self.regex_clear_button)
        layout.addWidget(self.regex_results_label)
        layout.addWidget(self.regex_results_box)
        
        self.regex_scraper_tab.setLayout(layout)

    def init_manual_regex_scraper_ui(self):
        layout = QVBoxLayout()

        # URL Input
        self.manual_regex_url_label = QLabel('Enter URL:')
        self.manual_regex_url_input = QTextEdit()
        self.manual_regex_url_input.setPlaceholderText('https://example.com')
        
        # Buttons
        self.manual_regex_generate_button = QPushButton('Generate Regex Pattern')
        self.manual_regex_generate_button.clicked.connect(self.generate_manual_regex_patterns)
        self.manual_regex_clear_button = QPushButton('Clear All')
        self.manual_regex_clear_button.clicked.connect(self.clear_all)

        # Generated Regex Pattern Box
        self.manual_regex_links_label = QLabel('Generated Regex Pattern:')
        self.manual_regex_links_box = QTextEdit()
        self.manual_regex_links_box.setReadOnly(True)
        
        # Add widgets to layout
        layout.addWidget(self.manual_regex_url_label)
        layout.addWidget(self.manual_regex_url_input)
        layout.addWidget(self.manual_regex_generate_button)
        layout.addWidget(self.manual_regex_clear_button)
        layout.addWidget(self.manual_regex_links_label)
        layout.addWidget(self.manual_regex_links_box)
        
        self.manual_regex_scraper_tab.setLayout(layout)

    def init_bulk_regex_scraper_ui(self):
        layout = QVBoxLayout()

        # URL Input
        self.bulk_regex_url_label = QLabel('Enter URLs (one per line):')
        self.bulk_regex_url_input = QTextEdit()
        self.bulk_regex_url_input.setPlaceholderText('Enter URLs here...')
        
        # Buttons
        self.bulk_regex_generate_button = QPushButton('Generate Bulk Regex Patterns')
        self.bulk_regex_generate_button.clicked.connect(self.generate_bulk_regex_patterns)
        self.bulk_regex_clear_button = QPushButton('Clear All')
        self.bulk_regex_clear_button.clicked.connect(self.clear_all)

        # Generated Regex Patterns Box
        self.bulk_regex_patterns_label = QLabel('Generated Regex Patterns:')
        self.bulk_regex_patterns_box = QTextEdit()
        self.bulk_regex_patterns_box.setReadOnly(True)
        
        # Add widgets to layout
        layout.addWidget(self.bulk_regex_url_label)
        layout.addWidget(self.bulk_regex_url_input)
        layout.addWidget(self.bulk_regex_generate_button)
        layout.addWidget(self.bulk_regex_clear_button)
        layout.addWidget(self.bulk_regex_patterns_label)
        layout.addWidget(self.bulk_regex_patterns_box)
        
        self.bulk_regex_scraper_tab.setLayout(layout)

    def scrape_links(self):
        url = self.url_input.toPlainText().strip()
        filename = self.filename_input.toPlainText().strip()
        if not url:
            self.captured_links_box.setPlainText('URL cannot be empty.')
            return
        
        # Automatically add .txt extension if not present
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        try:
            links = scrape_links(url)  # Use the function from scrape_links.py

            # Save links to file
            with open(filename, 'w') as file:
                for link in links:
                    file.write(f"{link}\n")
            
            # Display links in the box
            self.captured_links_box.clear()
            self.captured_links_box.setHtml('<br>'.join(f'<a href="{link}">{link}</a>' for link in links))
            
        except Exception as e:
            self.captured_links_box.setPlainText(f'Error: {str(e)}')

    def test_regex(self):
        pattern = self.regex_pattern_input.toPlainText().strip()
        test_string = self.regex_test_string_input.toPlainText().strip()
        if not pattern:
            self.regex_results_box.setPlainText('Pattern cannot be empty.')
            return

        try:
            matches = test_regex(pattern, test_string)  # Use the updated test_regex function
            self.regex_results_box.setPlainText('\n'.join(matches))
        except Exception as e:
            self.regex_results_box.setPlainText(f'Error: {str(e)}')

    def generate_manual_regex_patterns(self):
        url = self.manual_regex_url_input.toPlainText().strip()
        if not url:
            self.manual_regex_links_box.setPlainText('URL cannot be empty.')
            return

        try:
            pattern = generate_bulk_regex_patterns([url])  # Use the function from bulk_regex_generator.py
            self.manual_regex_links_box.setPlainText(pattern)
        except Exception as e:
            self.manual_regex_links_box.setPlainText(f'Error: {str(e)}')

    def generate_bulk_regex_patterns(self):
        urls = self.bulk_regex_url_input.toPlainText().strip().split('\n')
        if not urls:
            self.bulk_regex_patterns_box.setPlainText('No URLs provided.')
            return

        try:
            patterns = generate_bulk_regex_patterns(urls)  # Use the function from bulk_regex_generator.py
            self.bulk_regex_patterns_box.setPlainText('\n'.join(patterns))
        except Exception as e:
            self.bulk_regex_patterns_box.setPlainText(f'Error: {str(e)}')

    def clear_all(self):
        self.url_input.clear()
        self.filename_input.clear()
        self.captured_links_box.clear()
        self.regex_pattern_input.clear()
        self.regex_test_string_input.clear()
        self.regex_results_box.clear()
        self.manual_regex_url_input.clear()
        self.manual_regex_links_box.clear()
        self.bulk_regex_url_input.clear()
        self.bulk_regex_patterns_box.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LinkScraperApp()
    window.show()
    sys.exit(app.exec_())
