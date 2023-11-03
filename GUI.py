import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton

class SimpleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paper Please")
        self.setGeometry(100, 100, 1800, 900)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.output_field = QTextEdit()
        self.input_field = QLineEdit()
        self.submit_button = QPushButton("Send Message")

        self.submit_button.clicked.connect(self.display_text)

        layout.addWidget(self.output_field)
        layout.addWidget(self.input_field)
        layout.addWidget(self.submit_button)

        central_widget.setLayout(layout)

    def display_text(self):
        text = self.input_field.text()
        self.output_field.append(text)
        self.input_field.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec_())
