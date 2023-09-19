import sys
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QMessageBox
from SnagIt import SnippingTool
import OCR_From_Image as OCR
def exit_program():
    """Exit the application."""
    sys.exit()


class OCRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.snipping_tool_instance = None
        self.screenshot_path = None  # Initialize the screenshot_path attribute

        # Load the UI and initialize widgets
        self.fname = None
        self.ocr_result = None
        self._load_ui()
        self._initialize_widgets()

        # Show the app window
        self.show()

    def _load_ui(self):
        """Load the UI file and set up the interface."""
        uic.loadUi("OCR_From_image.ui", self)

    def _initialize_widgets(self):
        """Initialize and configure widgets."""

        # Widgets
        self.buttonCapture = self.findChild(QPushButton, "btnCapture")
        self.buttonOpenFile = self.findChild(QPushButton, "Button_Open_File")
        self.buttonConvert = self.findChild(QPushButton, "Button_Convert")
        self.buttonQuit = self.findChild(QPushButton, "Button_Quit")
        self.label = self.findChild(QLabel, "Label_Open_File")

        # Configure widgets
        self.label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse | QtCore.Qt.LinksAccessibleByMouse)
        self.buttonConvert.hide()

        # Connect signals to slots
        self.buttonCapture.clicked.connect(self.start_snipping)
        self.buttonOpenFile.clicked.connect(self.select_file)
        self.buttonConvert.clicked.connect(self.convert)
        self.buttonQuit.clicked.connect(exit_program)

    def convert(self):
        """Convert the selected file using OCR."""
        try:
            self.ocr_result = OCR.run_OCR(self.screenshot_path, r'C:\Program Files\Tesseract-OCR\tesseract',
                                          'text_extracted.txt')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to perform OCR with error: {e}")
        else:
            self.label.setText(self.ocr_result
                               )
            print(self.ocr_result)

    def start_snipping(self):
        self.snipping_tool_instance = SnippingTool(self)
        self.snipping_tool_instance.startSnipping()

    def handle_screenshot(self, pixmap):
        """Handle the captured screenshot."""
        self.screenshot_path = "screenshot.png"
        pixmap.save(self.screenshot_path)
        self.label.setText(f'Screenshot saved at {self.screenshot_path}')
        self.buttonConvert.show()  # Show the convert button after taking a screenshot

    def select_file(self):
        """Open a file dialog and select a file for OCR conversion."""
        file_filter = ("Image Files (*.jpg *.png *.bmp *.jfif *.gif);;"
                       "All Files (*)")
        self.fname = QFileDialog.getOpenFileName(self, "Select File to Convert", "", file_filter)

        if self.fname[0]:
            self.screenshot_path = self.fname[0]  # Update the screenshot_path attribute
            self.label.setText(f'File to Convert = {self.screenshot_path}')
            self.buttonConvert.show()


def main():
    app = QApplication(sys.argv)
    ocr_window = OCRApp()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
