import sys
import csv
import json
import pandas as pd
import conversation_utils
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QGridLayout, QWidget, QProgressBar
from conversation_utils import generate_single_conversation
from data_loader import load_text_data
from preloaded_data import load_data
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from conversation_utils import generate_single_conversation, generate_multiple_conversations

class NPCConversationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NPC Conversation Generator")
        self.setGeometry(100, 100, 600, 400)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(20, 250, 300, 25)

        self.input_csv_path = None
        self.faiss_index_path = None
        self.output_txt_path = None

        self.create_widgets()

    def create_widgets(self):
        layout = QGridLayout()

        self.faiss_index_button = QPushButton("Select FAISS Index")
        self.faiss_index_button.clicked.connect(self.select_faiss_index)
        layout.addWidget(self.faiss_index_button, 0, 0)

        self.input_csv_button = QPushButton("Select Input CSV")
        self.input_csv_button.clicked.connect(self.select_input_csv)
        layout.addWidget(self.input_csv_button, 1, 0)

        self.output_txt_button = QPushButton("Select Output TXT")
        self.output_txt_button.clicked.connect(self.select_output_txt)
        layout.addWidget(self.output_txt_button, 2, 0)

        self.generate_button = QPushButton("Generate Conversations")
        self.generate_button.clicked.connect(self.generate_conversations)
        layout.addWidget(self.generate_button, 3, 0)

        layout.addWidget(self.progress_bar, 4, 0, 1, 2)

        # Add labels for displaying file paths
        self.faiss_index_label = QLabel("")
        layout.addWidget(self.faiss_index_label, 0, 1)
        self.input_csv_label = QLabel("")
        layout.addWidget(self.input_csv_label, 1, 1)
        self.output_txt_label = QLabel("")
        layout.addWidget(self.output_txt_label, 2, 1)

        self.setLayout(layout)

    def select_faiss_index(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.faiss_index_path = QFileDialog.getExistingDirectory(self, "Select FAISS Index Folder", "", options=options)
        if self.faiss_index_path:
            self.faiss_index_label.setText(self.faiss_index_path)
        else:
            self.faiss_index_label.setText("No folder selected")

    def select_input_csv(self):
        self.input_csv_path = QFileDialog.getOpenFileName(self, "Select Input CSV")[0]
        if self.input_csv_path:
            self.input_csv_label.setText(self.input_csv_path)
        else:
            self.input_csv_label.setText("No file selected")

    def select_output_txt(self):
        self.output_txt_path = QFileDialog.getSaveFileName(self, "Select Output TXT")[0]
        if self.output_txt_path:
            self.output_txt_label.setText(self.output_txt_path)
        else:
            self.output_txt_label.setText("No file selected")

    def generate_conversations(self):
        # This function generates conversations and saves them into separate files with 4-digit numbering appended to the output_txt_path.
        
        if not self.input_csv_path or not self.faiss_index_path or not self.output_txt_path:
            print("Please select all required files.")
            return

        with open("chatcreat_prompt.txt", "r", encoding="utf-8") as f:
            system_message = f.read()

        db = FAISS.load_local(self.faiss_index_path, OpenAIEmbeddings())
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        with open(self.input_csv_path, "r", encoding="utf-8") as csvfile:
            input_csv = pd.read_csv(self.input_csv_path, header=None)
            num_rows = len(input_csv)
            self.progress_bar.setMinimum(0)
            self.progress_bar.setMaximum(num_rows)
            print(f"Processing row 0 of {num_rows}")
            for index, row in input_csv.iterrows():
                user_input_json = {
                    "Dict": row[0],
                    "Name": row[1],
                    "Emotion": row[2],
                }
                response_dict = conversation_utils.generate_single_conversation(self.faiss_index_path, user_input_json, system_message)
                formatted_response = json.loads(response_dict["output_text"])
                response_text = json.dumps(formatted_response, indent=2, ensure_ascii=False)

                # Generate a file name with 4-digit numbering
                output_file_name = f"{self.output_txt_path}_{index:04d}.json"
                
                # Write the response to a separate output file
                with open(output_file_name, "w", encoding="utf-8") as output_file:
                    output_file.write(f"{response_text}\n")

                self.progress_bar.setValue(index + 1)
                print(f"Processing row {index + 1} of {num_rows}")

        print("Conversations generated successfully!")

def main():
    app = QApplication(sys.argv)
    window = NPCConversationApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

