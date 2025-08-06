-- ===============================================
-- ANALYTICS_QUERIES.SQL
-- Key queries for dashboard data
-- ===============================================

-- 1. Overall sentiment distribution
SELECT 
    sentiment,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage
FROM sentiment_analysis
GROUP BY sentiment
ORDER BY count DESC;

-- 2. Sentiment by product/channel
SELECT 
    p.product_name,
    cf.channel,
    sa.sentiment,
    COUNT(*) as feedback_count,
    AVG(sa.sentiment_score) as avg_sentiment_score
FROM customer_feedback cf
JOIN products p ON cf.product_id = p.product_id
JOIN sentiment_analysis sa ON cf.feedback_id = sa.feedback_id
GROUP BY p.product_name, cf.channel, sa.sentiment
ORDER BY p.product_name, sa.sentiment;

-- 3. Top issues by frequency and severity
SELECT 
    issue_category,
    issue_description,
    severity,
    COUNT(*) as mentions,
    ROUND(AVG(CAST(cf.rating as FLOAT)), 2) as avg_rating
FROM issues_detected id
JOIN customer_feedback cf ON id.feedback_id = cf.feedback_id
GROUP BY issue_category, issue_description, severity
ORDER BY mentions DESC, severity DESC;

-- 4. Feature requests priority analysis
SELECT 
    feature_name,
    category,
    priority,
    COUNT(*) as requests,
    AVG(CAST(cf.rating as FLOAT)) as avg_user_rating
FROM feature_requests fr
JOIN customer_feedback cf ON fr.feedback_id = cf.feedback_id
GROUP BY feature_name, category, priority
ORDER BY requests DESC, priority DESC;

-- 5. Sentiment trend over time (last 30 days)
SELECT 
    CAST(cf.feedback_date as DATE) as date,
    sa.sentiment,
    COUNT(*) as daily_count,
    AVG(sa.sentiment_score) as avg_daily_sentiment
FROM customer_feedback cf
JOIN sentiment_analysis sa ON cf.feedback_id = sa.feedback_id
WHERE cf.feedback_date >= DATEADD(day, -30, GETDATE())
GROUP BY CAST(cf.feedback_date as DATE), sa.sentiment
ORDER BY date, sentiment;

-- 6. Dashboard summary metrics
SELECT 
    (SELECT COUNT(*) FROM customer_feedback WHERE feedback_date >= DATEADD(day, -7, GETDATE())) as total_feedback_7days,
    (SELECT COUNT(*) FROM sentiment_analysis WHERE sentiment = 'positive') as positive_count,
    (SELECT COUNT(*) FROM sentiment_analysis WHERE sentiment = 'negative') as negative_count,
    (SELECT COUNT(*) FROM sentiment_analysis WHERE sentiment = 'neutral') as neutral_count,
    (SELECT ROUND(AVG(sentiment_score), 2) FROM sentiment_analysis) as avg_sentiment_score,
    (SELECT AVG(CAST(rating as FLOAT)) FROM customer_feedback) as avg_rating;

-- 7. Recent feedback for dashboard table
SELECT TOP 10
    cf.feedback_text,
    sa.sentiment,
    sa.sentiment_score,
    p.product_name,
    CASE 
        WHEN EXISTS (SELECT 1 FROM issues_detected WHERE feedback_id = cf.feedback_id) THEN 'Issue'
        WHEN EXISTS (SELECT 1 FROM feature_requests WHERE feedback_id = cf.feedback_id) THEN 'Feature'
        ELSE 'General'
    END as category,
    cf.feedback_date
FROM customer_feedback cf
JOIN sentiment_analysis sa ON cf.feedback_id = sa.feedback_id
JOIN products p ON cf.product_id = p.product_id
ORDER BY cf.feedback_date DESC;
