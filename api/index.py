from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize global variables
db = None
qa_chain = None

def initialize_rag():
    global db, qa_chain
    
    # Load documents
    loader = DirectoryLoader(
        './knowledge_base',
        glob='**/*.txt',
        loader_cls=TextLoader,
        show_progress=True
    )
    documents = loader.load()
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)
    
    # Create embeddings and vector store
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv('GOOGLE_API_KEY')
    )
    
    db = FAISS.from_documents(texts, embeddings)
    
    # Create QA chain
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv('GOOGLE_API_KEY'),
        temperature=0.3,
        streaming=True
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(),
        return_source_documents=True
    )

# Initialize RAG on startup
initialize_rag()

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
            result = qa_chain({"query": query})
            
            # Prepare response data
            response_data = {
                "response": result['result'],
                "sources": [doc.metadata['source'] for doc in result['source_documents']]
            }
            
            yield f"data: {json.dumps(response_data)}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        yield 'data: [DONE]\n\n'
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
