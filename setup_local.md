# Local Development Setup

## Step 1: Install Python

### Option A: Install from Microsoft Store (Recommended for Windows)
1. Press `Win + S` and search for "Microsoft Store"
2. Search for "Python 3.10" or "Python 3.11"
3. Click "Install" or "Get"
4. Wait for installation to complete

### Option B: Download from python.org
1. Go to https://www.python.org/downloads/
2. Download Python 3.10.12 (or newer 3.10.x version)
3. Run the installer
4. **IMPORTANT**: Check "Add Python to PATH" during installation

## Step 2: Verify Installation

Open Command Prompt or PowerShell and run:
```bash
python --version
pip --version
```

You should see Python 3.10.x or higher.

## Step 3: Set Up Virtual Environment

```bash
# Navigate to project directory
cd "c:\Users\Rames\Desktop\my-ai-twin\my-rag-app"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows Command Prompt:
venv\Scripts\activate
# On Windows PowerShell:
venv\Scripts\Activate.ps1
```

## Step 4: Install Dependencies

```bash
# Make sure virtual environment is active (you'll see (venv) in prompt)
pip install -r requirements.txt
```

## Step 5: Set Up Environment Variables

Create a `.env` file in the project root:
```bash
# Create .env file
echo GOOGLE_API_KEY=your_google_api_key_here > .env
```

Replace `your_google_api_key_here` with your actual Google Gemini API key.

## Step 6: Run the Application

```bash
# Start the Flask server
python api/index.py
```

The app will be available at: http://localhost:5000

## Step 7: Access the Frontend

Open your web browser and go to:
http://localhost:5000

Or directly open the HTML file:
file:///c:/Users/Rames/Desktop/my-ai-twin/my-rag-app/public/index.html

## Troubleshooting

### If Python not found:
- Restart your command prompt after installation
- Try `py` instead of `python`
- Check if Python was added to PATH

### If pip not found:
- Use `python -m pip` instead of `pip`
- Ensure virtual environment is activated

### If dependencies fail:
- Update pip: `python -m pip install --upgrade pip`
- Try installing one by one if requirements.txt fails

### If API key error:
- Make sure `.env` file exists in the correct location
- Verify your Google Gemini API key is valid
- Check that the file is named exactly `.env` (not `.env.txt`)

## API Endpoints (Local)

- Health Check: http://localhost:5000/api/health
- Chat API: http://localhost:5000/api/chat (POST request)

## Testing the Chat

1. Open http://localhost:5000 in your browser
2. Type a message in the chat interface
3. The AI twin will respond based on the knowledge base

## Knowledge Base Files

Your AI twin's knowledge is stored in:
- `knowledge_base/profile.txt` - Basic profile information
- `knowledge_base/interests.txt` - Interests and hobbies  
- `knowledge_base/synthetic_future.txt` - Future aspirations

You can edit these files to customize your AI twin's responses!
