# My AI Twin

A RAG (Retrieval-Augmented Generation) powered AI twin application built with Flask and deployed on Vercel.

## Features

- **Knowledge Base**: Contains profile information, interests, and future aspirations
- **RAG Architecture**: Uses FAISS for vector similarity search
- **Google Gemini Integration**: Powered by Google's Gemini AI model
- **Web Interface**: Clean, responsive frontend for interacting with your AI twin

## Project Structure

```
my-rag-app/
├── api/
│   └── index.py          # Flask backend API
├── public/
│   └── index.html        # Frontend web interface
├── knowledge_base/       # AI twin's knowledge base
│   ├── profile.txt
│   ├── interests.txt
│   └── synthetic_future.txt
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel deployment configuration
└── .gitignore           # Git ignore file
```

## Setup Instructions

### 1. Environment Variables

This app requires a Google API key for Gemini integration:

```bash
GOOGLE_API_KEY=your_google_api_key_here
```

### 2. Local Development

1. Clone the repository:
```bash
git clone https://github.com/rameshtavishwakarma97-design/my-ai-twin.git
cd my-ai-twin/my-rag-app
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Add your GOOGLE_API_KEY to .env
```

5. Run the Flask app:
```bash
python api/index.py
```

### 3. Deployment on Vercel

1. Connect your GitHub repository to Vercel
2. Add the `GOOGLE_API_KEY` environment variable in Vercel dashboard
3. Deploy!

The app will be automatically deployed with the following configuration:
- Python 3.9 runtime
- API routes served from `/api/*`
- Static files served from `/`

## API Endpoints

- `POST /api/chat` - Chat with your AI twin
- `GET /api/` - Health check endpoint

## Technologies Used

- **Backend**: Flask, Python 3.9
- **AI/ML**: LangChain, Google Gemini, FAISS
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Vercel
- **Version Control**: Git, GitHub

## License

This project is open source and available under the [MIT License](LICENSE).
