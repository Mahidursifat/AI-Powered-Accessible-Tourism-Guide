import openai

class AccessibilityChatbot:
    def __init__(self, api_key):
        """Initialize OpenAI API with provided key"""
        openai.api_key = api_key
        
        # Predefined context for accessibility guidance
        self.system_context = (
            "You are a helpful AI assistant specializing in accessible travel. "
            "Your goal is to provide compassionate, detailed, and practical advice "
            "for travelers with various disabilities. Always prioritize safety, comfort, "
            "and independence in your recommendations."
        )
    
    def get_response(self, user_query):
        """Generate AI response to user query"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_context},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=300
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"I apologize, but I encountered an error processing your query: {str(e)}"
    
    def _validate_query(self, query):
        """Basic query validation"""
        if not query or len(query) < 3:
            raise ValueError("Query is too short. Please provide more details.")
        
        # Optional: Add more sophisticated query validation
        return True
