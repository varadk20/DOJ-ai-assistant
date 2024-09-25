import json
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

# Load JSON data from file
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

# Loop for asking user input
while True:
    # Get a question from the user
    question = input("Ask a question about the data (or type 'exit' to quit): ")

    if question.lower() == 'exit':
        print("Exiting program.")
        break

    # Check for specific footer link requests
    matched_footer_links = [link_text for link_text in footer_links.keys() if link_text.lower() in question.lower()]

    if matched_footer_links:
        # If there are matches, provide the corresponding URLs
        for link_text in matched_footer_links:
            url = footer_links[link_text]
            print(f"URL for '{link_text}': {url}")
        continue  # Skip model response if footer link is found

    # Format the prompt with context and question
    prompt = chat_prompt_template.format(context=context, question=question)

    # Get the answer from the model
    try:
        # Pass the prompt as a list
        answer = llm.generate([prompt])
        # Extract the text from the answer
        answer_text = answer.generations[0][0].text.strip()
        print("Answer:", answer_text)

    except Exception as e:
        print("Error occurred:", e)
