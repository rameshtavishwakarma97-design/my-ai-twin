from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import json
import numpy as np

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize global variables
knowledge_base = None
embeddings_model = None
llm = None

def load_knowledge_base():
    global knowledge_base, embeddings_model, llm
    
    # Simple knowledge base loading
    knowledge_base = {
        'profile': '',
        'interests': '',
        'synthetic_future': ''
    }
    
    # Load text files
    try:
        with open('./knowledge_base/profile.txt', 'r', encoding='utf-8') as f:
            knowledge_base['profile'] = f.read()
        with open('./knowledge_base/interests.txt', 'r', encoding='utf-8') as f:
            knowledge_base['interests'] = f.read()
        with open('./knowledge_base/synthetic_future.txt', 'r', encoding='utf-8') as f:
            knowledge_base['synthetic_future'] = f.read()
    except Exception as e:
        print(f"Error loading knowledge base: {e}")
    
    # Initialize embeddings
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv('GOOGLE_API_KEY')
    )
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv('GOOGLE_API_KEY'),
        temperature=0.3,
        streaming=True
    )

def simple_retrieval(query):
    """Simple keyword-based retrieval to avoid FAISS dependency"""
    query_lower = query.lower()
    relevant_docs = []
    
    for key, content in knowledge_base.items():
        if any(word in content.lower() for word in query_lower.split() if len(word) > 2):
            relevant_docs.append(content)
    
    # If no specific matches, return all content
    if not relevant_docs:
        relevant_docs = list(knowledge_base.values())
    
    return ' '.join(relevant_docs)

# Initialize on startup
load_knowledge_base()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    def generate():
        try:
            # Retrieve relevant context
            context = simple_retrieval(query)
            
            # Create prompt with context
            prompt = f"""You are an AI twin assistant. Use the following context to answer the user's question.

Context:
{context}

User Question: {query}

Provide a helpful and personalized response based on the context above."""
            
            # Generate response
            response = llm.invoke(prompt)
            
            response_data = {
                "response": response.content,
                "sources": ["knowledge_base"]
            }
            
            yield f"data: {json.dumps(response_data)}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        yield 'data: [DONE]\n\n'
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
