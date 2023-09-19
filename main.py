import sys
import traceback
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QMessageBox
from SpellChecker import spell_check_and_correct
from OCR_From_Image import run_OCR
from SnagIt import SnippingTool

# Move the styles to a separate CSS file and load it here
with open('styles.css', 'r') as f:
    STYLESHEET = f.read()

def save_to_file(filename, content):
    """Save content to a specified file."""
    with open(filename, 'w') as f:
        f.write(content)

def exit_program():
    """Exit the application."""
    sys.exit()

class OCRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.snipping_tool_instance = None
        self.screenshot_path = None

        # Load the UI and initialize widgets
        self.fname = None
        self.ocr_result = None
        self._load_ui()
        self._initialize_widgets()
        self.show()

    def _load_ui(self):
        """Load the UI file and set up the interface."""
        uic.loadUi("OCR_From_image.ui", self)

    def _initialize_widgets(self):
        """Initialize and configure widgets."""
        self.label = self.findChild(QLabel, "Label_Open_File")
        self.label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse | QtCore.Qt.LinksAccessibleByMouse)

        self.buttonConvert = self.findChild(QPushButton, "Button_Convert")
        self.buttonConvert.hide()

        for button_name, signal_handler in [("btnCapture", self.start_snipping),
                                            ("Button_Open_File", self.select_file),
                                            ("Button_Convert", self.convert),
                                            ("Button_Quit", exit_program)]:
            button = self.findChild(QPushButton, button_name)
            button.clicked.connect(signal_handler)

        # Apply the stylesheet for the buttons
        self.buttonConvert.setStyleSheet(STYLESHEET)
        self.findChild(QPushButton, "btnCapture").setStyleSheet(STYLESHEET)

    def convert(self):
        """Convert the selected file using OCR."""
        corrected_sentence = []
        try:
            self.ocr_result = run_OCR(self.screenshot_path, r'C:\\Program Files\\Tesseract-OCR\\tesseract',
                                      'text_extracted.txt')

            for i, result in enumerate(self.ocr_result.split('\n'), 0):
                if len(result) > 0:
                    corrected_sentence.append(spell_check_and_correct(result))
                    self.label.setText(corrected_sentence[-1])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to perform OCR with error: {e}")
            traceback.print_exc()
            pass

    def start_snipping(self):
        self.snipping_tool_instance = SnippingTool(self)
        self.snipping_tool_instance.startSnipping()

    def handle_screenshot(self, pixmap):
        """Handle the captured screenshot."""
        self.screenshot_path = "screenshot.png"
        pixmap.save(self.screenshot_path)
        self.label.setText(f'Screenshot saved at {self.screenshot_path}')
        self.buttonConvert.show()

    def select_file(self):
        """Open a file dialog and select a file for OCR conversion."""
        file_filter = "Image Files (*.jpg *.png *.bmp *.jfif *.gif);;All Files (*)"
        self.fname, _ = QFileDialog.getOpenFileName(self, "Select File to Convert", "", file_filter)

        if self.fname:
            self.screenshot_path = self.fname
            self.label.setText(f'File to Convert = {self.screenshot_path}')
            self.buttonConvert.show()

def main():
    app = QApplication(sys.argv)
    ocr_window = OCRApp()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
