Data Science Chatbot with Arxiv Integration
Overview
This project is an interactive chatbot that integrates the Arxiv API with a locally hosted Mistral-7B Instruct model. The chatbot allows users to query academic papers, receive concise summaries, and dive deeper into specific topics. It is designed to save time and provide insightful analyses for data science enthusiasts, researchers, and professionals.

Features
Search Academic Papers: Query the Arxiv API for papers on specific topics.
Summarization: Generate concise, informal summaries of academic papers using the Mistral model.
Deeper Analysis: Dive deeper into specific papers to extract key points and detailed insights.
Navigation: View multiple papers sequentially with options like "next" and "deeper."
Setup Instructions
Prerequisites
Python 3.9+
CUDA-compatible GPU (optional, but recommended for faster model inference)
Installed Python libraries (see requirements.txt).
Installation
Clone the Repository:

bash
Copy code
git clone [repository_link]
cd [repository_folder]
Set up a Virtual Environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Required Libraries:

bash
Copy code
pip install -r requirements.txt
Ensure Model Files are Downloaded: Place the Mistral-7B model files in the ./Mistral-7B-Instruct-v0.3 directory or update the script with your model path.

Running the Chatbot
Activate the virtual environment:

bash
Copy code
source venv/bin/activate  # On Windows: venv\Scripts\activate
Start the chatbot:

bash
Copy code
python data_science_chatbot.py
Interact with the chatbot:

Query papers using phrases like find papers on [topic].
Navigate papers using next.
Dive deeper into a paper with deeper.
Exit with exit.
Usage Examples
Sample Interaction
vbnet
Copy code
You: find papers on neural networks
Chatbot: Searching Arxiv for: neural networks...

Arxiv Results:
Paper 1: Lecture Notes: Neural Network Architectures
Abstract: These lecture notes provide an overview of Neural Network architectures from...

You: next
Chatbot: Displaying the next paper...

You: deeper
Chatbot: Diving deeper into: Lecture Notes: Neural Network Architectures
Detailed Analysis: These notes provide detailed insights into...
Limitations
Hardware Requirements: The model requires a GPU with sufficient memory for optimal performance.
Response Issues: Occasionally, model responses may repeat or truncate.
API Dependency: The chatbot is limited to the data available in the Arxiv API.
Future Improvements
Add support for other APIs (e.g., PubMed, IEEE).
Enhance the model’s ability to handle longer and more complex queries.
Improve inference speed by optimizing hardware usage or using smaller, fine-tuned models.

Author
Ethan Frenette

