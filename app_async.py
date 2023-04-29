import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit, QProgressBar, QCheckBox, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from preloaded_data import load_data
from conversation_utils import generate_single_conversation, generate_multiple_conversations

class LoadDataThread(QThread):
    finished = pyqtSignal()

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path

    def run(self):
        load_data(self.folder_path)
        self.finished.emit()


class GenerateConversationThread(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, faiss_index_path, user_input_json, system_message: str, use_multiple_responses):
        super().__init__()
        self.faiss_index_path = faiss_index_path
        self.user_input_json = user_input_json
        self.system_message = system_message
        self.use_multiple_responses = use_multiple_responses

    def run(self):
        if self.use_multiple_responses:
            response_dict = generate_multiple_conversations(self.faiss_index_path, self.user_input_json, self.system_message)
        else:
            response_dict = generate_single_conversation(self.faiss_index_path, self.user_input_json, self.system_message)
        self.finished.emit(response_dict)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def open_file_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.folder_input.setText(folder_path)

    def initUI(self):
        self.setWindowTitle('Chat Generator')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # ラベル
        folder_label = QLabel('Enter the path to the folder with text files:', self)
        layout.addWidget(folder_label)

        # フォルダパス入力欄
        self.folder_input = QLineEdit(self)
        layout.addWidget(self.folder_input)

        # ボタン
        self.load_data_button = QPushButton('Load data', self)
        self.load_data_button.clicked.connect(self.open_file_dialog)
        self.load_data_button.clicked.connect(self.load_data)
        layout.addWidget(self.load_data_button)

        # 入力欄
        self.dict_label = QLabel('Dict:', self)
        layout.addWidget(self.dict_label)
        self.dict_input = QLineEdit(self)
        layout.addWidget(self.dict_input)

        self.name_label = QLabel('Name:', self)
        layout.addWidget(self.name_label)
        self.name_input = QLineEdit(self)
        layout.addWidget(self.name_input)

        self.talk_label = QLabel('Talk:', self)
        layout.addWidget(self.talk_label)
        self.talk_input = QLineEdit(self)
        layout.addWidget(self.talk_input)

        self.behavior_label = QLabel('Behavior:', self)
        layout.addWidget(self.behavior_label)
        self.behavior_input = QLineEdit(self)
        layout.addWidget(self.behavior_input)

        self.emotion_label = QLabel('Emotion:', self)
        layout.addWidget(self.emotion_label)
        self.emotion_input = QLineEdit(self)
        layout.addWidget(self.emotion_input)

        self.request_label = QLabel('Request:', self)
        layout.addWidget(self.request_label)
        self.request_input = QLineEdit(self)
        layout.addWidget(self.request_input)

        self.multiple_responses_checkbox = QCheckBox('Use multiple responses', self)
        layout.addWidget(self.multiple_responses_checkbox)

        # ボタン
        self.generate_button = QPushButton('Generate conversation', self)
        self.generate_button.clicked.connect(self.generate_conversation)
        layout.addWidget(self.generate_button)

        # 出力欄
        self.output = QTextEdit(self)
        layout.addWidget(self.output)

        # プログレスバー
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

    def load_data(self):
        folder_path = self.folder_input.text()
        self.load_data_button.setEnabled(False)
        self.progress_bar.setValue(0)

        self.load_data_thread = LoadDataThread(folder_path)
        self.load_data_thread.finished.connect(self.on_load_data_finished)
        self.load_data_thread.start()

    def on_load_data_finished(self):
        self.load_data_button.setEnabled(True)
        self.progress_bar.setValue(100)

    def generate_conversation(self):
        user_dict = self.dict_input.text()
        name = self.name_input.text()
        talk = self.talk_input.text()
        behavior = self.behavior_input.text()
        emotion = self.emotion_input.text()
        request = self.request_input.text()

        user_input_json = {
            "dict": user_dict,
            "actions": [
                {
                    "name": name,
                    "talk": talk,
                    "behavior": behavior,
                    "emotion": emotion,
                },
            ],
            "request": request,
        }
        
        with open("system_prompt.txt", "r", encoding="utf-8") as f:
            system_message = f.read()

        use_multiple_responses = self.multiple_responses_checkbox.isChecked()
        self.generate_button.setEnabled(False)
        self.progress_bar.setValue(0)

        faiss_index_path = "faiss_index"
        self.generate_conversation_thread = GenerateConversationThread(faiss_index_path, user_input_json, system_message, use_multiple_responses)
        self.generate_conversation_thread.finished.connect(self.on_generate_conversation_finished)
        self.generate_conversation_thread.start()

    def on_generate_conversation_finished(self, response_dict):
        formatted_response = json.loads(response_dict["output_text"])
        response_text = json.dumps(formatted_response, indent=2, ensure_ascii=False)
        self.output.setPlainText(response_text)
        self.generate_button.setEnabled(True)
        self.progress_bar.setValue(100)

def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_app()
