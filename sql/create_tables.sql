-- ===============================================
-- CREATE_TABLES.SQL
-- Database schema for Customer Feedback Sentiment Analysis
-- ===============================================

-- Create database
CREATE DATABASE CustomerFeedbackDB;
USE CustomerFeedbackDB;

-- 1. Products table
CREATE TABLE products (
    product_id INT PRIMARY KEY IDENTITY(1,1),
    product_name VARCHAR(50) NOT NULL,
    category VARCHAR(30)
);

-- 2. Customer feedback table
CREATE TABLE customer_feedback (
    feedback_id INT PRIMARY KEY IDENTITY(1,1),
    customer_id VARCHAR(20),
    product_id INT,
    feedback_text NVARCHAR(MAX),
    rating INT CHECK (rating BETWEEN 1 AND 5),
    feedback_date DATE,
    channel VARCHAR(20), -- Mobile App, Website, Support
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 3. Sentiment analysis results table
CREATE TABLE sentiment_analysis (
    analysis_id INT PRIMARY KEY IDENTITY(1,1),
    feedback_id INT,
    sentiment VARCHAR(10) CHECK (sentiment IN ('positive', 'negative', 'neutral')),
    confidence_score DECIMAL(3,2), -- 0.00 to 1.00
    sentiment_score DECIMAL(4,2), -- -1.00 to 1.00
    analysis_date DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (feedback_id) REFERENCES customer_feedback(feedback_id)
);

-- 4. Issues tracking table
CREATE TABLE issues_detected (
    issue_id INT PRIMARY KEY IDENTITY(1,1),
    feedback_id INT,
    issue_category VARCHAR(50),
    issue_description VARCHAR(100),
    severity VARCHAR(10) CHECK (severity IN ('high', 'medium', 'low')),
    FOREIGN KEY (feedback_id) REFERENCES customer_feedback(feedback_id)
);

-- 5. Feature requests table
CREATE TABLE feature_requests (
    request_id INT PRIMARY KEY IDENTITY(1,1),
    feedback_id INT,
    feature_name VARCHAR(100),
    priority VARCHAR(10) CHECK (priority IN ('high', 'medium', 'low')),
    category VARCHAR(30),
    FOREIGN KEY (feedback_id) REFERENCES customer_feedback(feedback_id)
);

-- ===============================================
-- INSERT_SAMPLE_DATA.SQL
-- Sample data for testing and demonstration
-- ===============================================

-- Insert products
INSERT INTO products (product_name, category) VALUES
('Mobile App', 'Software'),
('Website', 'Software'),
('Customer Support', 'Service'),
('Logistics', 'Operations');

-- Insert sample feedback
INSERT INTO customer_feedback (customer_id, product_id, feedback_text, rating, feedback_date, channel) VALUES
('CUST001', 1, 'The new update is amazing! Love the dark mode feature.', 5, '2024-08-01', 'Mobile App'),
('CUST002', 1, 'App crashes frequently after the latest update', 1, '2024-08-02', 'Mobile App'),
('CUST003', 3, 'Customer service was helpful but response time could be better', 3, '2024-08-01', 'Support'),
('CUST004', 2, 'Payment process is seamless and secure', 5, '2024-08-03', 'Website'),
('CUST005', 2, 'The interface is confusing and hard to navigate', 2, '2024-08-02', 'Website'),
('CUST006', 4, 'Fast delivery and great product quality', 5, '2024-08-04', 'Website'),
('CUST007', 1, 'Search functionality needs improvement', 2, '2024-08-03', 'Mobile App'),
('CUST008', 3, 'Overall satisfied with the service', 4, '2024-08-04', 'Support'),
('CUST009', 1, 'Love the new features but app is slow', 3, '2024-08-05', 'Mobile App'),
('CUST010', 2, 'Website works perfectly on mobile devices', 5, '2024-08-05', 'Website');

-- Insert sentiment analysis results
INSERT INTO sentiment_analysis (feedback_id, sentiment, confidence_score, sentiment_score) VALUES
(1, 'positive', 0.95, 0.85),
(2, 'negative', 0.88, -0.72),
(3, 'neutral', 0.65, 0.15),
(4, 'positive', 0.92, 0.68),
(5, 'negative', 0.78, -0.55),
(6, 'positive', 0.89, 0.78),
(7, 'negative', 0.71, -0.42),
(8, 'positive', 0.83, 0.62),
(9, 'neutral', 0.69, 0.05),
(10, 'positive', 0.91, 0.74);

-- Insert detected issues
INSERT INTO issues_detected (feedback_id, issue_category, issue_description, severity) VALUES
(2, 'Performance', 'App crashes', 'high'),
(7, 'Features', 'Search functionality', 'medium'),
(5, 'UI/UX', 'Navigation confusion', 'medium'),
(9, 'Performance', 'Slow loading', 'medium');

-- Insert feature requests
INSERT INTO feature_requests (feedback_id, feature_name, priority, category) VALUES
(1, 'Dark mode', 'high', 'UI/UX'),
(7, 'Better search', 'medium', 'Features'),
(3, 'Faster response time', 'high', 'Service'),
(9, 'Performance optimization', 'high', 'Performance');
