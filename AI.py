import json
import sys
import time  # For simulating loading time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# Load JSON data from file - use your own path
file_path = "C:\\Users\\swaru\\Desktop\\myprojects\\DOJ-AI assistant\\myscrappeddata.json"

with open(file_path, 'r') as file:
    data = json.load(file)

# Prepare the context from the loaded JSON data
context = "\n".join([f"Card {item['card_number']}: {item['content']}" for item in data if item.get('content')])

# Extract footer links for easier reference
footer_links = {link['text']: link['url'] for link in data[-1]['footer_links']}

# Initialize the Ollama model
llm = Ollama(model="mistral")

# Create a ChatPromptTemplate with a formatted string
chat_prompt_template = ChatPromptTemplate.from_template(
    "You are a helpful assistant. Please provide the most relevant answer from the given file.\n\n"
    "Context:\n{context}\n\nQuestion: {question}\n"
    "Answer only with the most relevant information."
)


class Worker(QThread):
    result_ready = pyqtSignal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        # Simulate loading time (you can remove this sleep in a real application)
        time.sleep(1)  # Simulate waiting for the model response

        # Get the answer from the model
        try:
            answer = llm.generate([self.prompt])
            answer_text = answer.generations[0][0].text.strip()
            self.result_ready.emit(answer_text)
        except Exception as e:
            self.result_ready.emit(f"Error occurred: {str(e)}")


class DOJAIApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DOJ AI Assistant")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.question_label = QLabel("Enter your question:")
        layout.addWidget(self.question_label)

        self.question_entry = QLineEdit(self)
        layout.addWidget(self.question_entry)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_question)
        layout.addWidget(self.submit_button)

        self.loading_label = QLabel("")  # Loading message label
        layout.addWidget(self.loading_label)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def submit_question(self):
        question = self.question_entry.text()
        if question.lower() == 'exit':
            QApplication.quit()

        # Clear previous output
        self.output_text.clear()
        self.loading_label.setText("Loading...")  # Show loading message

        # Check for specific footer link requests
        matched_footer_links = [link_text for link_text in footer_links.keys() if link_text.lower() in question.lower()]

        if matched_footer_links:
            for link_text in matched_footer_links:
                url = footer_links[link_text]
                self.output_text.append(f"URL for '{link_text}': {url}")
            self.loading_label.clear()  # Clear loading message
            return  # Skip model response if footer link is found

        # Format the prompt with context and question
        prompt = chat_prompt_template.format(context=context, question=question)

        # Start the worker thread
        self.worker = Worker(prompt)
        self.worker.result_ready.connect(self.display_result)
        self.worker.start()

    def display_result(self, answer_text):
        self.output_text.append("Answer: " + answer_text)
        self.loading_label.clear()  # Clear loading message


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DOJAIApp()
    window.show()
    sys.exit(app.exec())
