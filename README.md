# Customer Insights Dashboard with Sentiment Analysis

A full-stack web application prototype that processes and classifies customer reviews using Natural Language Processing (NLP) and visualizes the insights on a dynamic, real-time dashboard.

## 📋 Project Overview

This project performs **Sentiment Analysis** on textual data to classify it as **Positive**, **Negative**, or **Neutral**. It combines a sophisticated data analysis backend (developed in a Python environment) with an interactive frontend to provide immediate insights into customer feedback.

The dashboard showcases key metrics, visualizes sentiment distribution, and allows for the real-time analysis of new customer reviews, simulating a complete end-to-end application.

## ✨ Features

- **Dynamic Dashboard**: An interactive and responsive interface built with Tailwind CSS and Chart.js to visualize sentiment data
- **Real-time Analysis**: Submit a new customer review and see its sentiment classification instantly update the dashboard metrics
- **Overall Sentiment Metrics**: Quickly view the total number of reviews and the percentage breakdown of positive, negative, and neutral sentiments
- **Sentiment Distribution**: A doughnut chart provides an at-a-glance view of the sentiment proportions
- **Detailed Review List**: Browse through recent reviews, each tagged with its classified sentiment and confidence score
- **In-depth Analysis Modal**: An integrated modal window explains the underlying data science process, tools, and methodologies used

## 🏗️ Architecture: From Prototype to Production

This repository contains a self-contained **prototype** that demonstrates the complete functionality of the application in a single HTML file. This approach is excellent for rapid development and showcasing the user experience.

### Current Architecture (Prototype)
```
Single HTML File
├── Frontend (HTML + CSS + JavaScript)
├── Simulated Backend Logic
└── Mock Data Storage
```

### Production-Ready Architecture

To transition this project to a true, production-ready full-stack application, the following architecture would be implemented:

#### Frontend
- The existing HTML, CSS, and JavaScript would be structured as a standalone frontend application (e.g., using a framework like **React** or **Vue**)
- Responsible for rendering the UI and making API calls

#### Backend API
- A dedicated server built using Python with a framework like **Flask** or **FastAPI**
- Hosts the trained NLP model
- Exposes API endpoints (e.g., `/api/reviews`, `/api/analyze`)
- The frontend communicates with this server instead of the current JavaScript simulation

#### Database
- A persistent database (like **PostgreSQL** or **MongoDB**) to store and manage all customer reviews
- The backend server handles all database interactions

```
Production Architecture
├── Frontend (React/Vue/Angular)
│   ├── Components
│   ├── Services (API calls)
│   └── State Management
├── Backend API (Flask/FastAPI)
│   ├── Routes/Endpoints
│   ├── NLP Model
│   ├── Business Logic
│   └── Database Integration
└── Database (PostgreSQL/MongoDB)
    ├── Reviews Collection
    ├── User Data
    └── Analytics Data
```

This separation of concerns is standard for scalable and maintainable web applications.

## 🔬 Data Analysis Engine

The core of this project is the NLP sentiment analysis model. Here's a breakdown of the process and technology behind it:

### Tools & Libraries Used

- **NLTK (Natural Language Toolkit)**: For text preprocessing, tokenization, and sentiment analysis
- **Pandas**: For efficient data manipulation and analysis
- **NumPy**: For numerical operations and handling arrays
- **Matplotlib & Seaborn**: To create visualizations showing sentiment distribution, word frequency, and trends

### Analysis Workflow

1. **Data Cleaning & Preprocessing**
   - Removing noise from text data
   - Stripping stop words
   - Performing tokenization to prepare the text for analysis

2. **Exploratory Data Analysis (EDA)**
   - Generating visual insights into the dataset
   - Understanding dataset characteristics and patterns

3. **Sentiment Classification**
   - Using a rule-based approach with NLTK's built-in Sentiment Analyzer (VADER)
   - Classifying text into positive, negative, or neutral categories

4. **Visualization**
   - Creating clear visual representations of sentiment outcomes
   - Communicating results effectively through charts and graphs

5. **Conclusion & Learnings**
   - Drawing insights and conclusions from the analysis
   - Identifying trends and patterns in customer feedback

## 🚀 Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Python 3.7+ (for backend development)
- Node.js (for production frontend setup)

### Running the Prototype
1. Clone this repository
2. Open `index.html` in your web browser
3. Interact with the dashboard and try the real-time sentiment analysis

### Setting Up for Development

#### Backend Setup
```bash
pip install nltk pandas numpy matplotlib seaborn flask
```

#### Frontend Setup (for production)
```bash
npm install react react-dom chart.js tailwindcss
```

## 📊 Dashboard Features

### Metrics Overview
- Total reviews processed
- Sentiment distribution percentages
- Real-time updates

### Interactive Charts
- Doughnut chart for sentiment distribution
- Historical trend analysis
- Confidence score visualization

### Review Management
- Add new reviews for instant analysis
- View detailed sentiment scores
- Browse historical review data

## 🛠️ Technical Implementation

### Sentiment Analysis Model
- **Algorithm**: VADER (Valence Aware Dictionary and sEntiment Reasoner)
- **Accuracy**: Rule-based approach optimized for social media text
- **Output**: Compound score ranging from -1 (most negative) to +1 (most positive)

### Frontend Technologies
- **Styling**: Tailwind CSS for responsive design
- **Charts**: Chart.js for interactive data visualization
- **JavaScript**: Vanilla JS for prototype, framework-ready for production

## 📈 Future Enhancements

- Machine learning model integration (BERT, RoBERTa)
- Multi-language sentiment analysis
- Advanced analytics and reporting
- User authentication and role management
- API rate limiting and caching
- Real-time notifications for sentiment alerts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- NLTK team for providing excellent NLP tools
- Chart.js community for visualization capabilities
- Tailwind CSS for the styling framework
- All contributors and testers who helped improve this project
