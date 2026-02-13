import sqlite3
from datetime import datetime
import os

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), 'portfolio.db')

def init_database():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create contacts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create stats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_count INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Initialize stats if not exists
    cursor.execute('SELECT COUNT(*) FROM stats')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO stats (visitor_count) VALUES (0)')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def add_contact(name, email, message):
    """Add a new contact form submission"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO contacts (name, email, message, created_at)
            VALUES (?, ?, ?, ?)
        ''', (name, email, message, datetime.now()))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding contact: {e}")
        return False

def get_all_contacts():
    """Retrieve all contact submissions"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, email, message, created_at
            FROM contacts
            ORDER BY created_at DESC
        ''')
        
        contacts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return contacts
    except Exception as e:
        print(f"Error retrieving contacts: {e}")
        return []

def increment_visitor_count():
    """Increment and return the visitor count"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE stats
            SET visitor_count = visitor_count + 1,
                last_updated = ?
            WHERE id = 1
        ''', (datetime.now(),))
        
        cursor.execute('SELECT visitor_count FROM stats WHERE id = 1')
        count = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        return count
    except Exception as e:
        print(f"Error incrementing visitor count: {e}")
        return 0

def get_visitor_count():
    """Get the current visitor count"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT visitor_count FROM stats WHERE id = 1')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    except Exception as e:
        print(f"Error getting visitor count: {e}")
        return 0

# Initialize database when module is imported
if __name__ == '__main__':
    init_database()
