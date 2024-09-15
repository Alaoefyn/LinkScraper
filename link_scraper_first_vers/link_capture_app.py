from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QMessageBox, QLineEdit, QLabel,
    QVBoxLayout, QWidget, QListWidget, QTextEdit, QAction, QFileDialog,
    QFormLayout, QProgressBar, QTabWidget, QCheckBox, QSpinBox
)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QFont

from scraper import fetch_html, filter_links, save_links_to_file, categorize_links, export_links
from scraper2 import fetch_html_with_fallback
from header_scraper import fetch_header_links
import sys

class LinkCaptureApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Link Capture App')
        self.setGeometry(100, 100, 800, 600)  # Adjusted size for more space

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget(self)
        self.layout.addWidget(self.tabs)

        self.create_capture_tab()
        self.create_fallback_tab()
        self.create_settings_tab()
        self.create_header_capture_tab()

        # Add Theme Toggle Button
        self.theme_toggle_button = QPushButton('Switch to Dark Mode', self)
        self.layout.addWidget(self.theme_toggle_button)
        self.theme_toggle_button.clicked.connect(self.toggle_theme)

        # Default theme is light
        self.is_dark_mode = False
        self.apply_light_mode()

        # Menu bar and actions
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu('File')

        self.save_action = QAction('Save Captured Links', self)
        self.save_action.triggered.connect(self.save_links)
        self.file_menu.addAction(self.save_action)

        self.export_csv_action = QAction('Export Links as CSV', self)
        self.export_csv_action.triggered.connect(lambda: self.export_links('csv'))
        self.file_menu.addAction(self.export_csv_action)

        self.export_json_action = QAction('Export Links as JSON', self)
        self.export_json_action.triggered.connect(lambda: self.export_links('json'))
        self.file_menu.addAction(self.export_json_action)

        self.copy_links_action = QAction('Copy Links to Clipboard', self)
        self.copy_links_action.triggered.connect(self.copy_links_to_clipboard)
        self.file_menu.addAction(self.copy_links_action)

    def create_capture_tab(self):
        capture_tab = QWidget()
        form_layout = QFormLayout()

        self.url_input = QLineEdit(self)
        form_layout.addRow(QLabel('Enter URL:'), self.url_input)

        self.filename_input = QLineEdit(self)
        form_layout.addRow(QLabel('Enter desired filename (without extension):'), self.filename_input)

        self.blacklist_input = QLineEdit(self)
        form_layout.addRow(QLabel('Enter blacklist keywords (comma separated):'), self.blacklist_input)

        self.whitelist_input = QLineEdit(self)
        form_layout.addRow(QLabel('Enter whitelist keywords (comma separated):'), self.whitelist_input)

        self.regex_input = QLineEdit(self)
        form_layout.addRow(QLabel('Enter regex pattern for filtering:'), self.regex_input)

        self.include_domains_input = QLineEdit(self)
        form_layout.addRow(QLabel('Include only specific domains (comma separated):'), self.include_domains_input)

        self.exclude_domains_input = QLineEdit(self)
        form_layout.addRow(QLabel('Exclude specific domains (comma separated):'), self.exclude_domains_input)

        self.button_capture = QPushButton('Capture All Links On Page', self)
        form_layout.addRow(self.button_capture)

        self.button_clear = QPushButton('Clear Inputs', self)
        form_layout.addRow(self.button_clear)

        self.progress_bar = QProgressBar(self)
        form_layout.addRow(QLabel('Progress:'), self.progress_bar)

        # Display captured links
        self.list_widget = QListWidget(self)
        form_layout.addRow(QLabel('Captured Links:'), self.list_widget)

        # Text area for displaying raw HTML (optional)
        self.text_edit_raw_html = QTextEdit(self)
        self.text_edit_raw_html.setReadOnly(True)
        form_layout.addRow(QLabel('Raw HTML (optional):'), self.text_edit_raw_html)

        capture_tab.setLayout(form_layout)
        self.tabs.addTab(capture_tab, "Capture Links")

        # Connect buttons to functions
        self.button_capture.clicked.connect(self.capture_links)
        self.button_clear.clicked.connect(self.clear_inputs)

    def create_fallback_tab(self):
        fallback_tab = QWidget()
        form_layout = QFormLayout()

        self.url_input_fallback = QLineEdit(self)
        form_layout.addRow(QLabel('Enter URL:'), self.url_input_fallback)

        self.filename_input_fallback = QLineEdit(self)
        form_layout.addRow(QLabel('Enter desired filename (without extension):'), self.filename_input_fallback)

        self.button_capture_fallback = QPushButton('Capture Links With Fallback', self)
        form_layout.addRow(self.button_capture_fallback)

        self.button_clear_fallback = QPushButton('Clear Inputs', self)
        form_layout.addRow(self.button_clear_fallback)

        self.progress_bar_fallback = QProgressBar(self)
        form_layout.addRow(QLabel('Progress:'), self.progress_bar_fallback)

        # Display captured links
        self.list_widget_fallback = QListWidget(self)
        form_layout.addRow(QLabel('Captured Links:'), self.list_widget_fallback)

        # Text area for displaying raw HTML (optional)
        self.text_edit_raw_html_fallback = QTextEdit(self)
        self.text_edit_raw_html_fallback.setReadOnly(True)
        form_layout.addRow(QLabel('Raw HTML (optional):'), self.text_edit_raw_html_fallback)

        fallback_tab.setLayout(form_layout)
        self.tabs.addTab(fallback_tab, "Fallback Scraper")

        # Connect buttons to functions
        self.button_capture_fallback.clicked.connect(self.capture_links_with_fallback)
        self.button_clear_fallback.clicked.connect(self.clear_inputs_fallback)

    def create_settings_tab(self):
        settings_tab = QWidget()
        form_layout = QFormLayout()

        self.auto_scrape_checkbox = QCheckBox('Enable automated scraping', self)
        form_layout.addRow(self.auto_scrape_checkbox)

        self.scrape_interval_spinbox = QSpinBox(self)
        self.scrape_interval_spinbox.setRange(1, 1440)
        self.scrape_interval_spinbox.setSuffix(' min')
        form_layout.addRow(QLabel('Scrape interval (minutes):'), self.scrape_interval_spinbox)

        settings_tab.setLayout(form_layout)
        self.tabs.addTab(settings_tab, "Settings")

        self.auto_scrape_checkbox.stateChanged.connect(self.toggle_automated_scraping)
        self.scrape_timer = QTimer(self)
        self.scrape_timer.timeout.connect(self.capture_links)

    def create_header_capture_tab(self):
        header_capture_tab = QWidget()
        form_layout = QFormLayout()

        self.url_input_header = QLineEdit(self)
        form_layout.addRow(QLabel('Enter URL:'), self.url_input_header)

        self.filename_input_header = QLineEdit(self)
        form_layout.addRow(QLabel('Enter desired filename (without extension):'), self.filename_input_header)

        self.button_capture_header = QPushButton('Capture Header Links', self)
        form_layout.addRow(self.button_capture_header)

        self.button_clear_header = QPushButton('Clear Inputs', self)
        form_layout.addRow(self.button_clear_header)

        self.progress_bar_header = QProgressBar(self)
        form_layout.addRow(QLabel('Progress:'), self.progress_bar_header)

        # Display captured links
        self.list_widget_header = QListWidget(self)
        form_layout.addRow(QLabel('Captured Header Links:'), self.list_widget_header)

        header_capture_tab.setLayout(form_layout)
        self.tabs.addTab(header_capture_tab, "Header Links")

        # Connect buttons to functions
        self.button_capture_header.clicked.connect(self.capture_header_links)
        self.button_clear_header.clicked.connect(self.clear_inputs_header)

    def toggle_theme(self):
        if self.is_dark_mode:
            self.apply_light_mode()
            self.theme_toggle_button.setText('Switch to Dark Mode')
        else:
            self.apply_dark_mode()
            self.theme_toggle_button.setText('Switch to Light Mode')
        self.is_dark_mode = not self.is_dark_mode

    def apply_dark_mode(self):
        with open('stylesdark.qss', 'r') as file:
            dark_stylesheet = file.read()
        self.setStyleSheet(dark_stylesheet)

    def apply_light_mode(self):
        with open('styleswhite.qss', 'r') as file:
            light_stylesheet = file.read()
        self.setStyleSheet(light_stylesheet)

    def capture_links(self):
        url = self.url_input.text()
        filename = self.filename_input.text()
        blacklist = self.blacklist_input.text().split(',')
        whitelist = self.whitelist_input.text().split(',')
        regex = self.regex_input.text()
        include_domains = self.include_domains_input.text().split(',')
        exclude_domains = self.exclude_domains_input.text().split(',')

        self.list_widget.clear()
        self.progress_bar.setValue(0)

        self.thread = LinkCaptureThread(url, blacklist, whitelist, regex, include_domains, exclude_domains)
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.captured_links.connect(self.display_captured_links)
        self.thread.raw_html.connect(self.display_raw_html)
        self.thread.start()

    def capture_links_with_fallback(self):
        url = self.url_input_fallback.text()
        filename = self.filename_input_fallback.text()

        self.list_widget_fallback.clear()
        self.progress_bar_fallback.setValue(0)

        self.thread_fallback = LinkCaptureThreadWithFallback(url)
        self.thread_fallback.progress.connect(self.progress_bar_fallback.setValue)
        self.thread_fallback.captured_links.connect(self.display_captured_links_fallback)
        self.thread_fallback.raw_html.connect(self.display_raw_html_fallback)
        self.thread_fallback.start()

    def capture_header_links(self):
        url = self.url_input_header.text()
        filename = self.filename_input_header.text()

        self.list_widget_header.clear()
        self.progress_bar_header.setValue(0)

        self.thread_header = HeaderLinkCaptureThread(url)
        self.thread_header.progress.connect(self.progress_bar_header.setValue)
        self.thread_header.captured_links.connect(self.display_captured_links_header)
        self.thread_header.start()

    def display_captured_links(self, links):
        self.list_widget.addItems(links)

    def display_captured_links_fallback(self, links):
        self.list_widget_fallback.addItems(links)

    def display_captured_links_header(self, links):
        self.list_widget_header.addItems(links)

    def display_raw_html(self, html):
        self.text_edit_raw_html.setPlainText(html)

    def display_raw_html_fallback(self, html):
        self.text_edit_raw_html_fallback.setPlainText(html)

    def clear_inputs(self):
        self.url_input.clear()
        self.filename_input.clear()
        self.blacklist_input.clear()
        self.whitelist_input.clear()
        self.regex_input.clear()
        self.include_domains_input.clear()
        self.exclude_domains_input.clear()
        self.list_widget.clear()
        self.text_edit_raw_html.clear()

    def clear_inputs_fallback(self):
        self.url_input_fallback.clear()
        self.filename_input_fallback.clear()
        self.list_widget_fallback.clear()
        self.text_edit_raw_html_fallback.clear()

    def clear_inputs_header(self):
        self.url_input_header.clear()
        self.filename_input_header.clear()
        self.list_widget_header.clear()

    def toggle_automated_scraping(self, state):
        if state == Qt.Checked:
            interval_minutes = self.scrape_interval_spinbox.value()
            interval_ms = interval_minutes * 60 * 1000
            self.scrape_timer.start(interval_ms)
        else:
            self.scrape_timer.stop()

    def save_links(self):
        links = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
        filename, _ = QFileDialog.getSaveFileName(self, 'Save Links', '', 'Text Files (*.txt);;All Files (*)')
        if filename:
            with open(filename, 'w') as file:
                file.write('\n'.join(links))
            QMessageBox.information(self, 'Success', 'Links saved successfully!')

    def export_links(self, file_format):
        links = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
        filename, _ = QFileDialog.getSaveFileName(self, f'Export Links as {file_format.upper()}', '', f'{file_format.upper()} Files (*.{file_format});;All Files (*)')
        if filename:
            export_links(links, filename, file_format)
            QMessageBox.information(self, 'Success', f'Links exported as {file_format.upper()} successfully!')

    def copy_links_to_clipboard(self):
        links = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
        clipboard = QApplication.clipboard()
        clipboard.setText('\n'.join(links))
        QMessageBox.information(self, 'Success', 'Links copied to clipboard!')

class LinkCaptureThread(QThread):
    progress = pyqtSignal(int)
    captured_links = pyqtSignal(list)
    raw_html = pyqtSignal(str)

    def __init__(self, url, blacklist, whitelist, regex, include_domains, exclude_domains):
        super().__init__()
        self.url = url
        self.blacklist = blacklist
        self.whitelist = whitelist
        self.regex = regex
        self.include_domains = include_domains
        self.exclude_domains = exclude_domains

    def run(self):
        links, raw_html = fetch_html(self.url)
        filtered_links = filter_links(links, self.blacklist, self.whitelist, self.regex, self.include_domains, self.exclude_domains)
        self.captured_links.emit(filtered_links)
        self.raw_html.emit(raw_html)

class LinkCaptureThreadWithFallback(QThread):
    progress = pyqtSignal(int)
    captured_links = pyqtSignal(list)
    raw_html = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        links, raw_html = fetch_html_with_fallback(self.url)
        self.captured_links.emit(links)
        self.raw_html.emit(raw_html)

class HeaderLinkCaptureThread(QThread):
    progress = pyqtSignal(int)
    captured_links = pyqtSignal(list)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        header_links = fetch_header_links(self.url)
        self.captured_links.emit(header_links)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LinkCaptureApp()
    window.show()
    sys.exit(app.exec_())
