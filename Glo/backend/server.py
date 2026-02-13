from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import os
import sys

# Add backend directory to path
sys.path.append(os.path.dirname(__file__))
from database import init_database, add_contact, get_visitor_count, increment_visitor_count, get_all_contacts

app = Flask(__name__, static_folder='../public')
CORS(app)

# Initialize database on startup
init_database()

# Serve static files
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/admin')
def admin():
    contacts = get_all_contacts()
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin - Contact Messages</title>
        <style>
            body { 
                font-family: 'Courier New', monospace; 
                background: #0a0a0a; 
                color: #00ff88; 
                padding: 20px; 
            }
            h1 { color: #00ff88; text-shadow: 0 0 10px #00ff88; }
            table { 
                border-collapse: collapse; 
                width: 100%; 
                margin-top: 20px;
                background: rgba(0, 255, 136, 0.1);
            }
            th, td { 
                border: 1px solid #00ff88; 
                padding: 12px; 
                text-align: left; 
            }
            th { background: rgba(0, 255, 136, 0.2); }
            tr:hover { background: rgba(0, 255, 136, 0.15); }
        </style>
    </head>
    <body>
        <h1>📬 Contact Messages</h1>
        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Message</th>
                <th>Date</th>
            </tr>
            {% for contact in contacts %}
            <tr>
                <td>{{ contact.id }}</td>
                <td>{{ contact.name }}</td>
                <td>{{ contact.email }}</td>
                <td>{{ contact.message }}</td>
                <td>{{ contact.created_at }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    
    return render_template_string(html, contacts=contacts)

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# API Routes
@app.route('/api/contact', methods=['POST'])
def contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        # Validate input
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()
        
        if not name or not email or not message:
            return jsonify({'error': 'All fields are required'}), 400
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email address'}), 400
        
        # Save to database
        success = add_contact(name, email, message)
        
        if success:
            return jsonify({
                'message': 'Thank you for your message! I will get back to you soon.',
                'success': True
            }), 200
        else:
            return jsonify({'error': 'Failed to save message. Please try again.'}), 500
            
    except Exception as e:
        print(f"Error in contact endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    """Return visitor statistics"""
    try:
        # Increment visitor count on each visit
        visitor_count = increment_visitor_count()
        
        return jsonify({
            'visitors': visitor_count,
            'success': True
        }), 200
        
    except Exception as e:
        print(f"Error in stats endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Server is running'
    }), 200

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Starting Glory's Portfolio Server")
    print("="*50)
    print("📍 Local:   http://localhost:5000")
    print("📍 Admin:   http://localhost:5000/admin")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
