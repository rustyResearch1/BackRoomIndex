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
    
    # Use environment variable for dreams file path if not provided
    dreams_path = dreams_file or os.getenv('DREAMS_FILE', 'dreams_dataset.json')
    
    # Initialize managers
    dreams_manager = DreamContextManager(dreams_path)
    anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/chat', methods=['POST'])
    def chat():
        try:
            message = request.json.get('message')
            response_text = dreams_manager.query_with_context(anthropic, message)
            return jsonify({"response": response_text})
        except Exception as e:
            print(f"Error in chat endpoint: {str(e)}")
            return jsonify({"response": "$ ERROR: Reality breach detected in backrooms subnet"}), 500

    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Create debug version of app
    debug_app = create_app()
    debug_app.debug = True  # Enable debug mode
    port = int(os.getenv('PORT', 5500))
    debug_app.run(host='0.0.0.0', port=port)