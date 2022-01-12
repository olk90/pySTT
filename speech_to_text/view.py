from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QTextEdit, QFileDialog

from common.view import load_ui_file
from logic import properties, convert_file, user_home


class PySSTMainWindow(QMainWindow):

    def __init__(self, form):
        super().__init__(parent=form)
        self.adjustSize()

        form.setWindowTitle("pySTT")
        form.resize(430, 220)

        self.layout = QVBoxLayout(form)

        ui_file_name = "ui/pystt_main.ui"
        ui_file = load_ui_file(ui_file_name)

        loader = QUiLoader()
        self.widget = loader.load(ui_file, form)
        ui_file.close()

        self.layout.addWidget(self.widget)

        # initialize fields
        self.input_edit: QTextEdit = self.widget.input_edit  # noqa
        self.output_edit: QTextEdit = self.widget.output_edit  # noqa

        self.lang_combo: QComboBox = self.widget.lang_combo  # noqa
        self.lang_combo.currentTextChanged.connect(self.set_input_lang)
        self.output_combo: QComboBox = self.widget.output_combo  # noqa

        self.input_button: QToolButton = self.widget.input_button  # noqa
        self.output_button: QToolButton = self.widget.output_button  # noqa
        self.process_button: QPushButton = self.widget.process_button  # noqa
        self.configure_buttons()

    def configure_buttons(self):
        self.input_button.clicked.connect(self.select_input_file)
        self.output_button.clicked.connect(self.select_output_path)
        self.process_button.clicked.connect(convert_file)

    def select_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   "Open WAV",
                                                   user_home,
                                                   "WAV files (*.wav)")
        properties.file_path = file_path
        self.input_edit.setText(file_path)

    def select_output_path(self):
        output_path = QFileDialog.getExistingDirectory(self,
                                                       "Output path",
                                                       user_home)

        properties.output_path = output_path
        self.output_edit.setText(output_path)

    def set_input_lang(self):
        input_lang = self.lang_combo.currentText()
        properties.input_lang = input_lang
