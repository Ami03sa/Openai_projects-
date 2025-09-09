# Openai_projects-
repo for all the openai promp engineering Projects
- Blog generator
- Movie recommender
- PDF RAG system
- Image creator 

🛠️ Setup Instructions

1. Clone this repo
```
git clone https://github.com/YOUR_USERNAME/openai-api-app.git
cd openai-api-app
```

3. Create a virtual environment (recommended)
```
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

5. Install dependencies
```
pip install -r requirements.txt
```


🔑 Set up API keys securely

Create a folder named .streamlit at the root of your project, and inside it create a file called secrets.toml.
```
mkdir .streamlit
nano .streamlit/secrets.toml


Paste your API keys inside:

OPENAI_API_KEY = "your_openai_api_key_here"
PINECONE_API_KEY = "your_pinecone_api_key_here"
PINECONE_ENVIRONMENT = "us-west1-gcp-free" # or your Pinecone env
```
⚠️ Important: The .streamlit folder is already in .gitignore so your secrets won’t be pushed to GitHub.

▶️ Run the app
```
streamlit run streamlit.py
```

This will start a local server. Open the link shown in the terminal (usually http://localhost:8501) in your browser.



