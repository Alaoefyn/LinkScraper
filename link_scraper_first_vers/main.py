import sys
from PyQt5.QtWidgets import QApplication
from link_capture_app import LinkCaptureApp

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # No need to load and apply the stylesheet here
    # The LinkCaptureApp class handles the theme switching and stylesheet loading

    window = LinkCaptureApp()
    window.show()
    sys.exit(app.exec_())



