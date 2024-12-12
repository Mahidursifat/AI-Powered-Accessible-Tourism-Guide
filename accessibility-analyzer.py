import openai
import re

class AccessibilityAnalyzer:
    def __init__(self, api_key):
        """Initialize OpenAI API with provided key"""
        openai.api_key = api_key
    
    def analyze_destination(self, destination):
        """Comprehensive accessibility analysis for a destination"""
        try:
            # Use OpenAI to analyze destination accessibility
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in travel accessibility for people with disabilities."},
                    {"role": "user", "content": f"Provide a comprehensive accessibility analysis for {destination}, including:"\
                        "1. Wheelchair accessibility of public spaces"\
                        "2. Transportation options for people with mobility challenges"\
                        "3. Availability of accessible accommodations"\
                        "4. Sensory-friendly attractions"\
                        "5. Overall accessibility rating out of 10"}
                ]
            )
            
            # Parse the AI response
            analysis_text = response.choices[0].message.content
            
            # Extract structured data
            return self._parse_accessibility_report(analysis_text)
        
        except Exception as e:
            raise ValueError(f"Destination analysis failed: {str(e)}")
    
    def _parse_accessibility_report(self, analysis_text):
        """Parse raw text into structured accessibility report"""
        report = {
            'overall_score': self._extract_score(analysis_text),
            'wheelchair_accessibility': self._extract_section(analysis_text, 'Wheelchair accessibility'),
            'transportation': self._extract_section(analysis_text, 'Transportation options'),
            'accommodations': self._extract_section(analysis_text, 'Accessible accommodations'),
            'sensory_attractions': self._extract_section(analysis_text, 'Sensory-friendly attractions')
        }
        return report
    
    def _extract_score(self, text):
        """Extract numerical accessibility score"""
        match = re.search(r'Overall accessibility rating[^\d]*(\d+(?:\.\d+)?)', text)
        return float(match.group(1)) if match else 0
    
    def _extract_section(self, text, section_name):
        """Extract specific section details"""
        pattern = rf'{section_name}:[^\n]*\n(.*?)(?=\n[A-Za-z]|\Z)'
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else "No specific information available."
