import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from database import AccessibilityDatabase
from accessibility_analyzer import AccessibilityAnalyzer
from chatbot import AccessibilityChatbot

# Load environment variables
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Initialize components
db = AccessibilityDatabase('accessibility_data.db')
analyzer = AccessibilityAnalyzer(os.getenv('OPENAI_API_KEY'))
chatbot = AccessibilityChatbot(os.getenv('OPENAI_API_KEY'))

@app.route('/analyze_destination', methods=['POST'])
def analyze_destination():
    """Analyze accessibility of a destination"""
    data = request.json
    destination = data.get('destination')
    
    try:
        # Analyze destination accessibility
        accessibility_report = analyzer.analyze_destination(destination)
        
        # Store analysis in database
        db.save_destination_analysis(destination, accessibility_report)
        
        return jsonify({
            'destination': destination,
            'accessibility_score': accessibility_report['overall_score'],
            'details': accessibility_report
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def accessibility_chat():
    """AI chatbot for accessibility queries"""
    data = request.json
    user_query = data.get('query')
    
    try:
        # Get chatbot response
        bot_response = chatbot.get_response(user_query)
        
        return jsonify({
            'response': bot_response
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create database tables
    db.create_tables()
    
    # Run the Flask application
    app.run(debug=True, port=5000)
