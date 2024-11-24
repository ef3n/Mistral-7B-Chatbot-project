"""
Data Science Chatbot with Arxiv Integration
===========================================

This script provides a chatbot that integrates with the Arxiv API to search for academic papers on data science topics. 
It also uses a local Mistral model to summarize and analyze text.

Features:
- Search for papers by topic using Arxiv API.
- Navigate through multiple papers with options to go 'next' or dive 'deeper'.
- Use a local language model for generating summaries and informal explanations.

How to Run:
1. Ensure the local model is downloaded and the required Python libraries are installed.
2. Run the script using Python 3.9+.
3. Interact with the chatbot by typing queries or asking to summarize topics.

Author: Ethan Frenette

"""

import requests
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Path to the local model directory
model_path = "./Mistral-7B-Instruct-v0.3"

# Load model and tokenizer
print("Loading the local model...")
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_path)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print(f"Model loaded successfully on device: {next(model.parameters()).device}")

# Helper Functions
def summarize_text(text):
    """
    Generate a concise summary using the model.
    """
    prompt = f"Summarize this text concisely:\n\n{text}\n\nSummary:"
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=1024
    )
    inputs = {k: v.to("cuda") for k, v in inputs.items()} if torch.cuda.is_available() else inputs

    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=150,
        temperature=0.3,
        do_sample=True,
        top_k=50,
        top_p=0.9,
        pad_token_id=tokenizer.pad_token_id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return clean_response(response)

def extract_key_points(text):
    """
    Extract key points from the provided text using the local model.
    """
    prompt = f"Extract the key points from this text:\n\n{text}\n\nKey points:"
    try:
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=1024
        )
        inputs = {k: v.to("cuda") for k, v in inputs.items()} if torch.cuda.is_available() else inputs

        outputs = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=100,
            temperature=0.3,
            do_sample=True,
            top_k=50,
            top_p=0.9,
            pad_token_id=tokenizer.pad_token_id
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return clean_response(response).split("\n")  # Split the response into a list of points
    except Exception as e:
        print(f"Error during key point extraction: {e}")
        return ["Key point extraction failed."]

def clean_response(response):
    """
    Remove repetitive or nonsensical sequences from the model's output.
    """
    sentences = response.split(". ")
    unique_sentences = []
    for sentence in sentences:
        if sentence not in unique_sentences:
            unique_sentences.append(sentence)
    return ". ".join(unique_sentences)

def dive_deeper(paper):
    """
    Provide a more detailed analysis of a given paper.
    """
    print(f"\nDiving deeper into: {paper['title']}")
    print(f"Full Abstract: {paper['summary']}")
    
    # Generate a more detailed summary
    detailed_summary = summarize_text(
        f"Summarize this abstract with a detailed explanation:\n\n{paper['summary']}\n\nBe clear, concise, and avoid repetition."
    )
    print(f"Detailed Analysis: {detailed_summary}\n")

    # Extract key points
    key_points = extract_key_points(paper['summary'])
    print("Key Points:")
    for point in key_points:
        print(f"- {point}")

def show_papers_with_options(papers):
    """
    Allow user to navigate through papers with options like 'next', 'deeper', or 'exit'.
    """
    current_paper_index = 0

    while True:
        paper = papers[current_paper_index]
        print(f"\nPaper {current_paper_index + 1}: {paper['title']}")
        print(f"Abstract: {paper['summary']}")
        
        user_input = input("Type 'next' to see the next paper, 'deeper' for detailed analysis, or 'exit' to quit: ").strip().lower()
        if user_input == "next":
            current_paper_index = (current_paper_index + 1) % len(papers)  # Cycle through papers
        elif user_input == "deeper":
            dive_deeper(paper)  # Call the deeper analysis function
        elif user_input == "exit":
            print("Exiting.")
            break
        else:
            print("Invalid input. Please type 'next', 'deeper', or 'exit'.")

def query_arxiv(query):
    """
    Query the Arxiv API for papers matching the given topic.
    """
    print(f"Searching Arxiv for: {query}")
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=3"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to query Arxiv API.")
        return None

def extract_paper_info(arxiv_data):
    """
    Extract paper titles and abstracts from the Arxiv API response.
    """
    import xml.etree.ElementTree as ET
    papers = []
    root = ET.fromstring(arxiv_data)
    ns = {'arxiv': 'http://www.w3.org/2005/Atom'}

    for entry in root.findall("arxiv:entry", ns):
        title = entry.find("arxiv:title", ns).text
        summary = entry.find("arxiv:summary", ns).text
        papers.append({"title": title, "summary": summary})
    
    return papers

# Main Execution
if __name__ == "__main__":
    print("Data Science Chatbot with Arxiv Integration. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip().lower()
        if user_input == "exit":
            print("Exiting chat. Goodbye!")
            break
        elif user_input.startswith("find papers on"):
            topic = user_input.replace("find papers on", "").strip()
            arxiv_data = query_arxiv(topic)
            if arxiv_data:
                papers = extract_paper_info(arxiv_data)
                if papers:
                    show_papers_with_options(papers)
                else:
                    print("No papers found.")
            else:
                print("Failed to query Arxiv. Please try again later.")
        else:
            # General chatbot functionality
            prompt = f"You are a helpful assistant. Respond politely and concisely.\nUser: {user_input}\nAssistant:"
            print("Model is thinking...")
            response = summarize_text(prompt)
            print(f"Model: {response}\n")
