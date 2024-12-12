import sqlite3
import json
from datetime import datetime

class AccessibilityDatabase:
    def __init__(self, db_path='accessibility_data.db'):
        """Initialize database connection"""
        self.db_path = db_path
    
    def create_tables(self):
        """Create necessary database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Destination accessibility analysis table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS destination_analyses (
                    id INTEGER PRIMARY KEY,
                    destination TEXT NOT NULL,
                    analysis_data TEXT NOT NULL,
                    overall_score REAL,
                    analyzed_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # User query history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS query_history (
                    id INTEGER PRIMARY KEY,
                    query TEXT NOT NULL,
                    response TEXT NOT NULL,
                    queried_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def save_destination_analysis(self, destination, analysis_data):
        """Save destination accessibility analysis"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO destination_analyses 
                (destination, analysis_data, overall_score) 
                VALUES (?, ?, ?)
            ''', (
                destination, 
                json.dumps(analysis_data), 
                analysis_data.get('overall_score', 0)
            ))
            conn.commit()
    
    def get_destination_analysis(self, destination):
        """Retrieve previous destination analysis"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT analysis_data, overall_score 
                FROM destination_analyses 
                WHERE destination = ? 
                ORDER BY analyzed_at DESC 
                LIMIT 1
            ''', (destination,))
            
            result = cursor.fetchone()
            return {
                'analysis': json.loads(result[0]) if result else None,
                'score': result[1] if result else None
            }
