from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic
import os
from dotenv import load_dotenv
from dreamcontext import DreamContextManager

# Load environment variables in development
if os.path.exists('.env'):
    load_dotenv()

def create_app(dreams_file: str = None):
    app = Flask(__name__, template_folder='.')
    
    # Debug print to check if API key is available (will show in Railway logs)
    api_key = os.getenv("ANTHROPIC_API_KEY")
    print(f"API Key available: {'Yes' if api_key else 'No'}")
    
    dreams_path = dreams_file or os.getenv('DREAMS_FILE', 'dreams_dataset.json')
    
    # Initialize managers
    dreams_manager = DreamContextManager(dreams_path)
    anthropic = Anthropic(api_key=api_key)

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/chat', methods=['POST'])
    def chat():
        try:
            message = request.json.get('message')
            
            # Debug prints
            print(f"Received message: {message}")
            print(f"Using API key: {'Yes' if os.getenv('ANTHROPIC_API_KEY') else 'No'}")
            
            response_text = dreams_manager.query_with_context(anthropic, message)
            return jsonify({"response": response_text})
        except Exception as e:
            error_msg = str(e)
            print(f"Detailed error in chat endpoint: {error_msg}")
            return jsonify({
                "response": f"$ ERROR: Connection issue\n# Debug info: {error_msg}"
            }), 500

    return app

app = create_app()

if __name__ == '__main__':
    debug_app = create_app()
    debug_app.debug = True
    port = int(os.getenv('PORT', 5000))
    debug_app.run(host='0.0.0.0', port=port)