- View 1: Main dashboard data
CREATE VIEW vw_dashboard_summary AS
SELECT 
    cf.feedback_id,
    cf.customer_id,
    p.product_name,
    cf.channel,
    cf.feedback_text,
    cf.rating,
    cf.feedback_date,
    sa.sentiment,
    sa.confidence_score,
    sa.sentiment_score,
    CASE 
        WHEN id.issue_id IS NOT NULL THEN id.issue_category
        WHEN fr.request_id IS NOT NULL THEN 'Feature Request'
        ELSE 'General Feedback'
    END as feedback_type,
    COALESCE(id.severity, fr.priority, 'normal') as priority_level
FROM customer_feedback cf
JOIN products p ON cf.product_id = p.product_id
JOIN sentiment_analysis sa ON cf.feedback_id = sa.feedback_id
LEFT JOIN issues_detected id ON cf.feedback_id = id.feedback_id
LEFT JOIN feature_requests fr ON cf.feedback_id = fr.feedback_id;

-- View 2: Time series data for trends
CREATE VIEW vw_sentiment_trends AS
SELECT 
    CAST(cf.feedback_date as DATE) as date,
    p.product_name,
    cf.channel,
    sa.sentiment,
    COUNT(*) as feedback_count,
    AVG(sa.sentiment_score) as avg_sentiment_score,
    AVG(CAST(cf.rating as FLOAT)) as avg_rating
FROM customer_feedback cf
JOIN products p ON cf.product_id = p.product_id
JOIN sentiment_analysis sa ON cf.feedback_id = sa.feedback_id
GROUP BY CAST(cf.feedback_date as DATE), p.product_name, cf.channel, sa.sentiment;

-- View 3: Issues and requests summary
CREATE VIEW vw_issues_requests AS
SELECT 
    'Issue' as type,
    id.issue_category as category,
    id.issue_description as description,
    id.severity as priority,
    COUNT(*) as count,
    AVG(CAST(cf.rating as FLOAT)) as avg_rating
FROM issues_detected id
JOIN customer_feedback cf ON id.feedback_id = cf.feedback_id
GROUP BY id.issue_category, id.issue_description, id.severity

UNION ALL

SELECT 
    'Feature Request' as type,
    fr.category,
    fr.feature_name as description,
    fr.priority,
    COUNT(*) as count,
    AVG(CAST(cf.rating as FLOAT)) as avg_rating
FROM feature_requests fr
JOIN customer_feedback cf ON fr.feedback_id = cf.feedback_id
GROUP BY fr.category, fr.feature_name, fr.priority;
