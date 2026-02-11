# My AI Twin

A memory-efficient RAG (Retrieval-Augmented Generation) powered AI twin application built with Flask and optimized for Vercel deployment.

## Features

- **Memory Efficient**: Optimized for serverless environments with minimal memory footprint
- **Knowledge Base**: Contains profile information, interests, and future aspirations
- **Lightweight RAG**: Uses keyword-based retrieval instead of heavy vector databases
- **Google Gemini Integration**: Powered by Google's Gemini AI model
- **Web Interface**: Clean, responsive frontend for interacting with your AI twin
- **Production Ready**: Built with error handling, timeouts, and resource limits

## Project Structure

```
my-rag-app/
├── api/
│   └── index.py          # Flask backend API (memory-optimized)
├── public/
│   └── index.html        # Frontend web interface
├── knowledge_base/       # AI twin's knowledge base
│   ├── profile.txt
│   ├── interests.txt
│   └── synthetic_future.txt
├── requirements.txt      # Minimal Python dependencies
├── vercel.json          # Optimized Vercel deployment configuration
├── .python-version      # Python version specification
├── .gitignore           # Comprehensive git ignore
└── vercel-ignore.txt    # Vercel build exclusions
```

## Optimizations for Vercel

### Memory Management
- **Bundle Size**: Reduced to ~25MB (well under 250MB limit)
- **Function Memory**: Limited to 512MB RAM
- **Response Limits**: Max 1000 tokens, 500 character responses
- **Query Limits**: Maximum 500 character input

### Dependencies
- **Minimal Requirements**: Only 7 essential packages
- **Removed Heavy Dependencies**: No FAISS, sentence-transformers, or large ML libraries
- **Python 3.11**: Stable and compatible runtime

### Error Handling
- **Graceful Degradation**: Fallback responses for errors
- **Timeout Protection**: 30-second LLM timeout
- **Input Validation**: Size limits and sanitization
- **Health Checks**: Detailed status monitoring

## Setup Instructions

### 1. Environment Variables

Required environment variables for deployment:

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

### 3. Vercel Deployment

1. **Connect Repository**:
   - Go to [vercel.com](https://vercel.com)
   - Click "Import Project" and connect your GitHub repository
   - Select the `my-rag-app` folder

2. **Configure Environment Variables**:
   - In Vercel dashboard, add `GOOGLE_API_KEY` 
   - Set any other required environment variables

3. **Deploy**:
   - The app will automatically deploy with optimized settings
   - Bundle size: ~25MB
   - Memory limit: 512MB
   - Function timeout: 10 seconds

## API Endpoints

- `GET /api/health` - Health check with status details
- `POST /api/chat` - Chat with your AI twin (streaming response)

### Health Check Response
```json
{
  "status": "healthy",
  "llm_initialized": true,
  "knowledge_loaded": true
}
```

### Chat Request
```json
{
  "query": "What are your interests?"
}
```

### Chat Response (Streaming)
```
data: {"response": "I'm interested in...", "sources": ["knowledge_base"]}
data: [DONE]
```

## Deployment Limits Compliance

✅ **Bundle Size**: ~25MB (under 250MB limit)  
✅ **Function Memory**: 512MB (under 1GB limit)  
✅ **Build Time**: < 1 minute (under 45 minute limit)  
✅ **Response Time**: < 10 seconds (under timeout limit)  
✅ **Dependencies**: Minimal, compatible packages  

## Monitoring

- **Health Endpoint**: `/api/health` for status monitoring
- **Error Handling**: Comprehensive error responses
- **Resource Limits**: Built-in memory and time limits
- **Logging**: Structured error logging for debugging

## Technologies Used

- **Backend**: Flask, Python 3.11
- **AI/ML**: LangChain, Google Gemini (lightweight integration)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Vercel (optimized configuration)
- **Version Control**: Git, GitHub

## Troubleshooting

### Common Issues

1. **Out of Memory Errors**: 
   - Fixed with 512MB memory limit and response size limits
   - Minimal dependency footprint

2. **Build Failures**:
   - Python version specified in `.python-version`
   - Optimized `vercel.json` configuration

3. **Timeout Issues**:
   - 10-second function timeout
   - 30-second LLM timeout

4. **Bundle Size Issues**:
   - Reduced to ~25MB from ~250MB
   - Removed heavy ML dependencies

## License

This project is open source and available under the [MIT License](LICENSE).
