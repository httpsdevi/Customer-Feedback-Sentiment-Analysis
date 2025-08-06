"""
Customer Feedback Sentiment Analysis Pipeline
Processes customer feedback and stores results in SQL Server database
"""

import pandas as pd
import numpy as np
import pyodbc
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import logging
from datetime import datetime

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

class SentimentAnalyzer:
    def __init__(self, connection_string):
        """Initialize the sentiment analyzer with database connection"""
        self.connection_string = connection_string
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        
        # Keywords for issue detection
        self.issue_keywords = {
            'performance': ['slow', 'crash', 'freeze', 'lag', 'loading', 'timeout'],
            'ui_ux': ['confusing', 'difficult', 'hard', 'navigate', 'interface', 'design'],
            'payment': ['payment', 'billing', 'charge', 'refund', 'transaction'],
            'features': ['missing', 'need', 'want', 'request', 'add', 'feature']
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def clean_text(self, text):
        """Clean and preprocess text"""
        if pd.isna(text):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text

    def analyze_sentiment_textblob(self, text):
        """Analyze sentiment using TextBlob"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
            
        return sentiment, abs(polarity), polarity

    def analyze_sentiment_vader(self, text):
        """Analyze sentiment using VADER"""
        scores = self.vader_analyzer.polarity_scores(text)
        compound_score = scores['compound']
        
        if compound_score >= 0.05:
            sentiment = 'positive'
        elif compound_score <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
            
        confidence = max(scores['pos'], scores['neg'], scores['neu'])
        
        return sentiment, confidence, compound_score

    def detect_issues(self, text, feedback_id):
        """Detect issues in feedback text"""
        text_lower = text.lower()
        detected_issues = []
        
        for category, keywords in self.issue_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # Determine severity based on context
                    if any(urgent in text_lower for urgent in ['urgent', 'critical', 'broken', 'crash']):
                        severity = 'high'
                    elif any(moderate in text_lower for moderate in ['slow', 'sometimes', 'occasionally']):
                        severity = 'medium'
                    else:
                        severity = 'low'
                    
                    detected_issues.append({
                        'feedback_id': feedback_id,
                        'issue_category': category.replace('_', '/').title(),
                        'issue_description': f"{keyword.title()} related issue",
                        'severity': severity
                    })
                    break  # Only one issue per category
                    
        return detected_issues

    def detect_feature_requests(self, text, feedback_id):
        """Detect feature requests in feedback"""
        text_lower = text.lower()
        feature_requests = []
        
        # Common feature request patterns
        request_patterns = [
            r'need.*(?:feature|option|ability)',
            r'want.*(?:feature|option|ability)',
            r'request.*(?:feature|option|ability)',
            r'would.*like.*(?:feature|option|ability)',
            r'please.*add',
            r'should.*have'
        ]
        
        for pattern in request_patterns:
            if re.search(pattern, text_lower):
                # Extract potential feature name
                words = word_tokenize(text_lower)
                words = [w for w in words if w not in self.stop_words and len(w) > 2]
                
                # Determine priority based on keywords
                if any(high_priority in text_lower for high_priority in ['urgent', 'really', 'desperately', 'badly']):
                    priority = 'high'
                elif any(medium_priority in text_lower for medium_priority in ['would like', 'prefer', 'nice']):
                    priority = 'medium'
                else:
                    priority = 'low'
                
                feature_requests.append({
                    'feedback_id': feedback_id,
                    'feature_name': f"Requested feature from feedback {feedback_id}",
                    'priority': priority,
                    'category': 'General'
                })
                break
                
        return feature_requests

    def get_unprocessed_feedback(self):
        """Get feedback that hasn't been processed yet"""
        query = """
        SELECT cf.feedback_id, cf.feedback_text, cf.rating
        FROM customer_feedback cf
        LEFT JOIN sentiment_analysis sa ON cf.feedback_id = sa.feedback_id
        WHERE sa.feedback_id IS NULL
        """
        
        try:
            conn = pyodbc.connect(self.connection_string)
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            self.logger.error(f"Error getting unprocessed feedback: {e}")
            return pd.DataFrame()

    def save_sentiment_results(self, results):
        """Save sentiment analysis results to database"""
        if not results:
            return
            
        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            
            for result in results:
                cursor.execute("""
                    INSERT INTO sentiment_analysis 
                    (feedback_id, sentiment, confidence_score, sentiment_score, analysis_date)
                    VALUES (?, ?, ?, ?, ?)
                """, 
                result['feedback_id'],
                result['sentiment'],
                result['confidence'],
                result['sentiment_score'],
                datetime.now()
                )
            
            conn.commit()
            conn.close()
            self.logger.info(f"Saved {len(results)} sentiment results")
            
        except Exception as e:
            self.logger.error(f"Error saving sentiment results: {e}")

    def save_issues(self, issues):
        """Save detected issues to database"""
        if not issues:
            return
            
        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            
            for issue in issues:
                cursor.execute("""
                    INSERT INTO issues_detected 
                    (feedback_id, issue_category, issue_description, severity)
                    VALUES (?, ?, ?, ?)
                """, 
                issue['feedback_id'],
                issue['issue_category'],
                issue['issue_description'],
                issue['severity']
                )
            
            conn.commit()
            conn.close()
            self.logger.info(f"Saved {len(issues)} issues")
            
        except Exception as e:
            self.logger.error(f"Error saving issues: {e}")

    def save_feature_requests(self, requests):
        """Save feature requests to database"""
        if not requests:
            return
            
        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            
            for request in requests:
                cursor.execute("""
                    INSERT INTO feature_requests 
                    (feedback_id, feature_name, priority, category)
                    VALUES (?, ?, ?, ?)
                """, 
                request['feedback_id'],
                request['feature_name'],
                request['priority'],
                request['category']
                )
            
            conn.commit()
            conn.close()
            self.logger.info(f"Saved {len(requests)} feature requests")
            
        except Exception as e:
            self.logger.error(f"Error saving feature requests: {e}")

    def process_feedback(self):
        """Main processing function"""
        self.logger.info("Starting feedback processing...")
        
        # Get unprocessed feedback
        feedback_df = self.get_unprocessed_feedback()
        
        if feedback_df.empty:
            self.logger.info("No new feedback to process")
            return
        
        self.logger.info(f"Processing {len(feedback_df)} feedback items...")
        
        sentiment_results = []
        all_issues = []
        all_requests = []
        
        for _, row in feedback_df.iterrows():
            feedback_id = row['feedback_id']
            text = row['feedback_text']
            
            # Clean text
            cleaned_text = self.clean_text(text)
            
            if not cleaned_text:
                continue
            
            # Analyze sentiment using both methods and combine
            tb_sentiment, tb_confidence, tb_score = self.analyze_sentiment_textblob(cleaned_text)
            vader_sentiment, vader_confidence, vader_score = self.analyze_sentiment_vader(cleaned_text)
            
            # Use VADER as primary, TextBlob as secondary
            final_sentiment = vader_sentiment
            final_confidence = vader_confidence
            final_score = vader_score
            
            # Store results
            sentiment_results.append({
                'feedback_id': feedback_id,
                'sentiment': final_sentiment,
                'confidence': round(final_confidence, 2),
                'sentiment_score': round(final_score, 2)
            })
            
            # Detect issues and feature requests
            issues = self.detect_issues(cleaned_text, feedback_id)
            requests = self.detect_feature_requests(cleaned_text, feedback_id)
            
            all_issues.extend(issues)
            all_requests.extend(requests)
        
        # Save all results
        self.save_sentiment_results(sentiment_results)
        self.save_issues(all_issues)
        self.save_feature_requests(all_requests)
        
        self.logger.info(f"Processing complete: {len(sentiment_results)} sentiments, {len(all_issues)} issues, {len(all_requests)} requests")

    def generate_summary_report(self):
        """Generate a summary report of recent analysis"""
        try:
            conn = pyodbc.connect(self.connection_string)
            
            # Get overall sentiment distribution
            sentiment_query = """
            SELECT sentiment, COUNT(*) as count 
            FROM sentiment_analysis 
            GROUP BY sentiment
            """
            sentiment_df = pd.read_sql(sentiment_query, conn)
            
            # Get top issues
            issues_query = """
            SELECT issue_category, COUNT(*) as count 
            FROM issues_detected 
            GROUP BY issue_category 
            ORDER BY count DESC
            """
            issues_df = pd.read_sql(issues_query, conn)
            
            # Get top feature requests
            requests_query = """
            SELECT feature_name, COUNT(*) as count 
            FROM feature_requests 
            GROUP BY feature_name 
            ORDER BY count DESC
            """
            requests_df = pd.read_sql(requests_query, conn)
            
            conn.close()
            
            print("=== SENTIMENT ANALYSIS SUMMARY ===")
            print(sentiment_df)
            print("\n=== TOP ISSUES ===")
            print(issues_df.head())
            print("\n=== TOP FEATURE REQUESTS ===")
            print(requests_df.head())
            
        except Exception as e:
            self.logger.error(f"Error generating summary: {e}")


# Main execution
if __name__ == "__main__":
    # Database connection string
    CONNECTION_STRING = """
    Driver={ODBC Driver 17 for SQL Server};
    Server=localhost;
    Database=CustomerFeedbackDB;
    Trusted_Connection=yes;
    """
    
    # Initialize analyzer
    analyzer = SentimentAnalyzer(CONNECTION_STRING)
    
    # Process new feedback
    analyzer.process_feedback()
    
    # Generate summary report
    analyzer.generate_summary_report()

# Additional utility functions
def batch_process_csv(csv_file_path, connection_string):
    """Process feedback from CSV file and insert into database"""
    try:
        # Read CSV file
        df = pd.read_csv(csv_file_path)
        
        # Connect to database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # Insert feedback data
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO customer_feedback 
                (customer_id, product_id, feedback_text, rating, feedback_date, channel)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
            row['customer_id'],
            row['product_id'], 
            row['feedback_text'],
            row['rating'],
            row['feedback_date'],
            row['channel']
            )
        
        conn.commit()
        conn.close()
        print(f"Successfully processed {len(df)} records from CSV")
        
    except Exception as e:
        print(f"Error processing CSV: {e}")

def create_powerbi_export():
    """Export data in Power BI friendly format"""
    CONNECTION_STRING = """
    Driver={ODBC Driver 17 for SQL Server};
    Server=localhost;
    Database=CustomerFeedbackDB;
    Trusted_Connection=yes;
    """
    
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        
        # Export main dashboard view
        main_query = """
        SELECT * FROM vw_dashboard_summary
        ORDER BY feedback_date DESC
        """
        main_df = pd.read_sql(main_query, conn)
        main_df.to_csv('powerbi_export_main.csv', index=False)
        
        # Export trend data
        trend_query = """
        SELECT * FROM vw_sentiment_trends
        ORDER BY date DESC
        """
        trend_df = pd.read_sql(trend_query, conn)
        trend_df.to_csv('powerbi_export_trends.csv', index=False)
        
        # Export issues and requests
        issues_query = """
        SELECT * FROM vw_issues_requests
        ORDER BY count DESC
        """
        issues_df = pd.read_sql(issues_query, conn)
        issues_df.to_csv('powerbi_export_issues.csv', index=False)
        
        conn.close()
        
        print("Power BI export files created:")
        print("- powerbi_export_main.csv")
        print("- powerbi_export_trends.csv") 
        print("- powerbi_export_issues.csv")
        
    except Exception as e:
        print(f"Error creating Power BI export: {e}")

# Automated scheduling function
def schedule_analysis():
    """Function to be called by task scheduler"""
    import time
    
    CONNECTION_STRING = """
    Driver={ODBC Driver 17 for SQL Server};
    Server=localhost;
    Database=CustomerFeedbackDB;
    Trusted_Connection=yes;
    """
    
    analyzer = SentimentAnalyzer(CONNECTION_STRING)
    
    while True:
        try:
            print(f"Running scheduled analysis at {datetime.now()}")
            analyzer.process_feedback()
            
            # Wait for 1 hour before next run
            time.sleep(3600)
            
        except KeyboardInterrupt:
            print("Scheduled analysis stopped")
            break
        except Exception as e:
            print(f"Error in scheduled analysis: {e}")
            time.sleep(300)  # Wait 5 minutes before retry
