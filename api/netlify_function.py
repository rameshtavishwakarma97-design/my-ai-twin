from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import os
import json
import sys

app = Flask(__name__)
CORS(app)

# Initialize global variables
knowledge_base = None
llm = None

def load_knowledge_base():
    global knowledge_base, llm
    
    try:
        # Simple knowledge base loading with memory efficiency
        knowledge_base = {
            'profile': '',
            'interests': '',
            'synthetic_future': ''
        }
        
        # Load text files with error handling
        files = {
            'profile': './knowledge_base/profile.txt',
            'interests': './knowledge_base/interests.txt',
            'synthetic_future': './knowledge_base/synthetic_future.txt'
        }
        
        for key, file_path in files.items():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    knowledge_base[key] = f.read().strip()
            except FileNotFoundError:
                print(f"Warning: {file_path} not found")
                knowledge_base[key] = ""
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                knowledge_base[key] = ""
        
        # Initialize LLM with minimal configuration
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        # Import here to avoid build issues
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0.3,
                streaming=True,
                max_tokens=1000,
                timeout=30
            )
        except ImportError as e:
            print(f"Failed to import ChatGoogleGenerativeAI: {e}")
            llm = None
        
        print("Knowledge base and LLM initialized successfully")
        
    except Exception as e:
        print(f"Initialization error: {e}")
        knowledge_base = {'profile': '', 'interests': '', 'synthetic_future': ''}
        llm = None

def simple_retrieval(query):
    """Memory-efficient keyword-based retrieval"""
    if not knowledge_base:
        return ""
    
    query_lower = query.lower()
    relevant_docs = []
    
    # Simple keyword matching with memory efficiency
    for key, content in knowledge_base.items():
        if content and any(word in content.lower() for word in query_lower.split() if len(word) > 2):
            relevant_docs.append(content)
    
    # If no specific matches, return all content (limited)
    if not relevant_docs:
        all_content = ' '.join(knowledge_base.values())
        return all_content[:2000] if len(all_content) > 2000 else all_content
    
    # Limit combined content size
    combined = ' '.join(relevant_docs)
    return combined[:2000] if len(combined) > 2000 else combined

# Initialize on startup with error handling
load_knowledge_base()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "llm_initialized": llm is not None,
        "knowledge_loaded": bool(knowledge_base and any(knowledge_base.values()))
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint with memory efficiency and error handling"""
    if not llm:
        return jsonify({"error": "LLM not initialized. Check environment variables."}), 500
    
    data = request.json
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # Limit query length to prevent memory issues
    if len(query) > 500:
        return jsonify({"error": "Query too long. Maximum 500 characters allowed."}), 400
    
    def generate():
        try:
            # Retrieve relevant context
            context = simple_retrieval(query)
            
            # Create prompt with size limits
            prompt = f"""You are an AI twin assistant. Use the following context to answer the user's question concisely.

Context:
{context[:1000]}

User Question: {query}

Provide a helpful and personalized response based on the context above. Keep your response under 200 words."""
            
            # Generate response with error handling
            response = llm.invoke(prompt)
            
            response_data = {
                "response": response.content[:500] if response.content else "I apologize, but I couldn't generate a response.",
                "sources": ["knowledge_base"]
            }
            
            yield f"data: {json.dumps(response_data)}\n\n"
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            print(error_msg)
            yield f"data: {json.dumps({'error': error_msg})}\n\n"
        
        yield 'data: [DONE]\n\n'
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "Request entity too large"}), 413

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

# Netlify serverless function handler
def handler(request):
    return app(request.environ, lambda status, headers: None)

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=False)
