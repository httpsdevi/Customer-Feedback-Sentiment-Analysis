# Customer Feedback Sentiment Analysis System 2025

## 📊 Project Overview

This project presents a dynamic web application designed for real-time sentiment analysis of customer feedback. Utilizing a state-of-the-art pre-trained RoBERTa model, it classifies incoming feedback into positive, negative, or neutral sentiments. The system provides an interactive dashboard for visualizing sentiment distribution and reviewing individual feedback entries.

The application is architected with a Flask backend responsible for handling the API and sentiment analysis, complemented by a modern and responsive HTML/CSS/JavaScript frontend to ensure an engaging user experience.

## ✨ Key Features

* **Real-time Sentiment Analysis:** Leverages the `cardiffnlp/twitter-roberta-base-sentiment` model for accurate and instant sentiment classification.
* **Interactive Dashboard:**
    * **Live Sentiment Counts:** Displays real-time, animated counts of positive, negative, and neutral feedback.
    * **Visual Distribution:** An intuitive doughnut chart visualizes the overall sentiment breakdown.
    * **Recent Feedback Stream:** A chronological list of submitted feedback, complete with sentiment badges and timestamps.
    * **Dynamic Filtering:** Easily filter the recent feedback list by sentiment type (All, Positive, Negative, Neutral).
    * **Smooth Animations:** Engaging hover effects, card animations, and counter transitions.
    * **Keyboard Shortcuts:** Press `Ctrl+Enter` to quickly submit feedback.
* **Persistent Data Storage:** All submitted feedback and their analyzed sentiments are securely stored in a local SQLite database (`sentiment.db`).
* **Modern & Responsive UI:** Crafted with a clean, intuitive, and mobile-friendly interface that adapts seamlessly to all screen sizes.
* **Automatic Updates:** Dashboard data automatically refreshes every 30 seconds to reflect the latest insights.
* **Developer-Friendly Architecture:** Clear separation of frontend and backend concerns for easier development and maintenance.

## 🚀 Technologies Used

### Backend:
* **Python 3.x**
* **Flask:** Web framework for building the API endpoints
* **Transformers (Hugging Face):** Essential for loading and utilizing the RoBERTa sentiment model
* **PyTorch / NumPy / SciPy:** Core libraries underpinning the model's operation and numerical computations
* **SQLite3:** A lightweight, serverless database for local data persistence

### Frontend:
* **HTML5 & CSS3:** For structuring and styling a modern, engaging user interface
* **JavaScript (ES6+):** Powers dynamic interactions, asynchronous API calls, and chart rendering
* **Chart.js:** An open-source JavaScript library for creating interactive data visualizations
* **Google Fonts (Poppins):** Enhances typography for a professional look
* **CSS Animations:** Smooth transitions and hover effects for enhanced user experience

## 🛠️ Setup and Installation

Follow these steps to set up and run the project on your local machine.

### 1. Clone the Repository

First, clone the project from GitHub:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

*(**Important:** Remember to replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name.)*

### 2. Create and Activate a Python Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Required Python Dependencies

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

**Required packages in `requirements.txt`:**
```
flask
transformers
torch
scipy
numpy
huggingface_hub
```

### 4. Configure Hugging Face Cache Directory (Optional but Recommended)

The RoBERTa model is approximately 500MB and is downloaded by the `transformers` library to a default cache location (typically `C:\Users\<YourUsername>\.cache\huggingface`). If your C: drive has limited space, you can redirect this cache to another drive (e.g., D:).

**For the current terminal session:**

* **Windows PowerShell:**
    ```powershell
    $env:HF_HOME="D:\huggingface_cache"
    ```
* **macOS/Linux (Bash/Zsh):**
    ```bash
    export HF_HOME="/path/to/your/preferred/cache/directory"
    ```

**For permanent system-wide configuration (Windows):**
1. Search for "Edit the system environment variables" in your Start Menu
2. Click the "Environment Variables..." button
3. Under "User variables for [Your Username]", click "New..."
4. Set `Variable name`: `HF_HOME`
5. Set `Variable value`: `D:\huggingface_cache` (or your desired path on D:)
6. Click OK on all windows. **A terminal/IDE restart is required for changes to take effect.**

### 5. Run the Flask Application

Start the backend server by executing `app.py`:

```bash
python app.py
```

Upon its first run, the application will:
* Download the RoBERTa model (this might take a few minutes depending on your internet connection and cache settings)
* Initialize and create the `sentiment.db` SQLite database file in the project's root directory

The server will start at `http://127.0.0.1:5000`

### 6. Access the Dashboard

Once the Flask application is running, open your web browser and navigate to:

**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

## 💡 How to Use the Dashboard

### Submitting Feedback

1. **Enter Feedback:** Type or paste customer feedback into the "Submit New Feedback" textarea
2. **Analyze:** Click the "Analyze & Save" button or press `Ctrl+Enter`
3. **View Result:** The sentiment (Positive, Negative, or Neutral) will be displayed with color-coded styling
4. **Clear:** Use the "Clear" button to reset the input field

### Monitoring Dashboard

* **Live Statistics Cards:** 
  - View animated counters showing total counts for each sentiment category
  - Color-coded cards (Green for Positive, Red for Negative, Yellow for Neutral)

* **Sentiment Distribution Chart:**
  - Interactive doughnut chart displaying proportional breakdown
  - Hover over sections to see exact counts
  - Automatically updates with new submissions

* **Recent Feedback List:**
  - Chronological display of all submitted feedback
  - Each entry shows sentiment badge and relative timestamp
  - Color-coded left border indicates sentiment type

### Filtering Feedback

* Click the filter buttons above the Recent Feedback section:
  - **All:** Display all feedback entries
  - **Positive:** Show only positive feedback
  - **Negative:** Show only negative feedback  
  - **Neutral:** Show only neutral feedback

### Auto-Refresh

* Dashboard automatically updates every 30 seconds
* No manual refresh needed for continuous monitoring

## 🌐 Project Structure

```
.
├── app.py                     # Flask backend: API endpoints, sentiment analysis, DB interaction
├── templates/
│   └── index.html             # Frontend: HTML structure, CSS styling, JavaScript logic
├── sentiment.db               # SQLite database file (auto-generated on first run)
└── README.md                  # This project documentation file
```

## 📡 API Endpoints

The Flask backend exposes the following REST API endpoints:

### 1. Analyze Sentiment
* **Endpoint:** `/analyze`
* **Method:** POST
* **Request Body:** 
  ```json
  {
    "text": "Your feedback text here"
  }
  ```
* **Response:**
  ```json
  {
    "sentiment": "positive|negative|neutral"
  }
  ```

### 2. Get Dashboard Statistics
* **Endpoint:** `/dashboard_data`
* **Method:** GET
* **Response:**
  ```json
  {
    "positive": 42,
    "negative": 15,
    "neutral": 23
  }
  ```

### 3. Get Recent Feedback
* **Endpoint:** `/recent_feedback`
* **Method:** GET
* **Response:**
  ```json
  {
    "feedback": [
      {
        "text": "Great service!",
        "sentiment": "positive",
        "timestamp": "2025-11-02T10:30:00"
      }
    ]
  }
  ```

## 🎨 Dashboard Features

### Visual Design
* **Modern Gradient Backgrounds:** Subtle purple-blue gradient theme
* **Glassmorphism Effects:** Semi-transparent cards with backdrop blur
* **Smooth Animations:** Fade-in effects, hover transitions, and animated counters
* **Responsive Grid Layout:** Automatically adapts to screen size
* **Color-Coded Sentiments:** 
  - 🟢 Green for Positive
  - 🔴 Red for Negative
  - 🟡 Yellow for Neutral

### Interactive Elements
* **Hover Effects:** Cards lift and cast stronger shadows on hover
* **Button Animations:** Scale and shadow transitions on interaction
* **Filter Toggle:** Active state highlighting for selected filters
* **Loading States:** Visual feedback during analysis
* **Empty States:** Friendly messages when no data is available

### User Experience
* **Keyboard Navigation:** Tab through inputs, use shortcuts
* **Error Handling:** Clear error messages for failed operations
* **Input Validation:** Prevents empty submissions
* **Responsive Design:** Works on desktop, tablet, and mobile devices
* **Accessibility:** Semantic HTML and proper contrast ratios

## 🧑‍💻 Development Insight

This project began its journey within a Google Colab environment. This allowed for rapid prototyping, efficient model loading, and iterative testing of the core sentiment analysis logic leveraging Colab's free GPU resources. Once the analysis pipeline was robust, it was refactored and integrated into this Flask web application to create a fully interactive and standalone dashboard.

### Model Information
* **Sentiment Model:** [cardiffnlp/twitter-roberta-base-sentiment](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment)
* **Model Size:** ~500MB
* **Framework:** Transformers (Hugging Face)
* **Base Model:** RoBERTa (Robustly Optimized BERT Pretraining Approach)

### Database Schema

**Table: `feedback`**
```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    sentiment TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Troubleshooting

### Model Download Issues
* **Problem:** Model fails to download
* **Solution:** Check internet connection and HF_HOME path permissions

### Port Already in Use
* **Problem:** Flask can't start on port 5000
* **Solution:** Change port in `app.py` or stop other services using port 5000

### Database Lock Error
* **Problem:** SQLite database is locked
* **Solution:** Close other connections or restart the Flask application

### Missing Dependencies
* **Problem:** Import errors when running `app.py`
* **Solution:** Ensure all packages in `requirements.txt` are installed

## 🚀 Future Enhancements

Potential features for future versions:

- [ ] Export feedback data to CSV/Excel
- [ ] Date range filtering for feedback
- [ ] Sentiment trend analysis over time
- [ ] Multi-language support
- [ ] User authentication and role-based access
- [ ] Email notifications for negative feedback
- [ ] Advanced analytics and reporting
- [ ] Batch import of feedback from files
- [ ] API rate limiting and authentication
- [ ] Docker containerization

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/httpsdevi/Customer-Feedback-Sentiment-Analysis/issues).

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open-source and released under the [MIT License](https://opensource.org/licenses/MIT).

## 👨‍💻 Author

**Your Name**
- GitHub: [httpsdevi](https://github.com/httpsdevi)
- LinkedIn: [DEBLINA MANDAL](https://www.linkedin.com/in/deblina-mandal-615507273/)

## 🙏 Acknowledgments

* [Hugging Face](https://huggingface.co/) for the Transformers library and model hosting
* [Cardiff NLP](https://github.com/cardiffnlp) for the sentiment analysis model
* [Chart.js](https://www.chartjs.org/) for the beautiful data visualizations
* [Flask](https://flask.palletsprojects.com/) for the lightweight web framework

---

⭐ **If you found this project helpful, please give it a star!** ⭐
