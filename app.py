# No more 'import mysql.connector'
import sqlite3 
from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np
import os # Added to check for database file

# --- 1. Initialize Flask App ---
app = Flask(__name__)

# --- 2. Define Database File ---
DATABASE_FILE = 'sentiment.db'

# --- 3. Load RoBERTa Model ---
print("Loading RoBERTa model... This may take a moment.")
MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    print("RoBERTa model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
# --------------------------------------------------------------------------

# --- 4. SQLite Database Functions (Replaces MySQL) ---

# Helper function to get a new database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    # This line makes it return data as dictionaries (like {'sentiment': 'positive'})
    conn.row_factory = sqlite3.Row 
    return conn

# New function to create the table if it doesn't exist
def init_db():
    # Check if the database file already exists
    if os.path.exists(DATABASE_FILE):
        return # Database is already set up

    print("Creating new database and table...")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # This is the same SQL command you used for MySQL
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database 'sentiment.db' created successfully.")
    except Exception as e:
        print(f"Error creating database: {e}")

# --------------------------------------------------------------------------

# --- 5. RoBERTa Helper Functions (No Changes) ---
def polarity_scores_roberta(example):
  encoded_text = tokenizer(example, return_tensors='pt', truncation=True, max_length=512)
  output = model(**encoded_text)
  scores = output[0][0].detach().numpy()
  scores = softmax(scores)
  scores_dict = {
    'roberta_neg' : scores[0],
    'roberta_neu' : scores[1],
    'roberta_pos' : scores[2]
  }
  return scores_dict

def get_sentiment_label(scores_dict):
    label = max(scores_dict, key=scores_dict.get)
    if label == 'roberta_pos': return 'positive'
    elif label == 'roberta_neg': return 'negative'
    else: return 'neutral'
# --------------------------------------------------------------------------


# --- 6. Flask Routes (API) ---

# ROUTE 1: Home Page (No Change)
@app.route('/')
def home():
    return render_template('index.html')


# ROUTE 2: Analyze Endpoint (Slightly Modified for SQLite)
@app.route('/analyze', methods=['POST'])
def analyze_feedback():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    feedback_text = data['text']

    # 1. Analyze sentiment (No Change)
    scores = polarity_scores_roberta(feedback_text)
    sentiment = get_sentiment_label(scores)

    # 2. Save to SQLite Database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # SQLite uses '?' as a placeholder instead of '%s'
        sql = "INSERT INTO feedback (content, sentiment) VALUES (?, ?)"
        val = (feedback_text, sentiment)
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database error on insert: {e}")
    
    # 3. Return result (No Change)
    return jsonify({'sentiment': sentiment})


# ROUTE 3: Dashboard Data (Slightly Modified for SQLite)
@app.route('/dashboard_data', methods=['GET'])
def dashboard_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    sql = "SELECT sentiment, COUNT(*) as count FROM feedback GROUP BY sentiment"
    cursor.execute(sql)
    results = cursor.fetchall() # This will now be a list of dicts
    cursor.close()
    conn.close()

    # Format data for Chart.js
    data = {'positive': 0, 'negative': 0, 'neutral': 0}
    for row in results:
        if row['sentiment'] in data:
            data[row['sentiment']] = row['count']
            
    return jsonify(data)

# --------------------------------------------------------------------------

# --- 7. Run the Application ---
if __name__ == '__main__':
    init_db() # Call the function to create the DB and table
    app.run(debug=True)