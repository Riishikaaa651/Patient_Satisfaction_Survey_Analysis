# 🏥 MedInsight AI

**Intelligent Insights. Better Care.**

A premium SaaS-style Patient Satisfaction Intelligence Platform built with Streamlit. Transform raw patient survey data into actionable clinical insights using AI-powered analytics, sentiment analysis, and automated recommendations.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Overview

MedInsight AI is an end-to-end analytics platform designed for healthcare organizations to analyze patient satisfaction surveys. It combines natural language processing, sentiment analysis, and machine learning to provide:

- **Automated Data Processing** - Clean, validate, and preprocess survey data
- **AI-Powered Sentiment Analysis** - VADER-based sentiment scoring
- **Issue Categorization** - Automatic classification of patient complaints
- **Priority Scoring** - Intelligent ranking of critical cases
- **Department Benchmarking** - Comparative performance analytics
- **Actionable Recommendations** - Data-driven improvement suggestions
- **Interactive Dashboards** - Modern glassmorphism UI with real-time filtering

Built for the **HCL Internship Project** - Patient Satisfaction Analytics.

---

## ✨ Key Features

### 📊 **Comprehensive Analytics Pipeline**
- **Data Validation** - Healthcare-specific guardrails ensure only patient satisfaction datasets are accepted
- **Automated Cleaning** - Handle missing values, normalize ratings, parse dates
- **Feature Engineering** - Extract word count, response length, NPS categories
- **Text Preprocessing** - Tokenization, stopword removal, lemmatization

### 💬 **Sentiment & NLP Analysis**
- **VADER Sentiment Scoring** - Compound sentiment scores (-1 to +1)
- **Sentiment Classification** - Positive, Neutral, Negative labels
- **Issue Categorization** - Classify feedback into:
  - Waiting Time
  - Staff Behaviour
  - Cleanliness
  - Billing Issues
  - Medical Care Quality
  - General Feedback
- **Text Summarization** - Automated department-level summaries with deduplication

### ⚡ **Priority & Action Mapping**
- **Priority Scoring (0-10)** - Weighted algorithm considering:
  - Inverted rating (low rating = high priority)
  - Negative sentiment intensity
  - Feedback length (detailed complaints)
  - Critical issue categories
- **Priority Labels** - 🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low
- **Recommended Actions** - Automated action mapping per priority level

### 🏆 **Department Benchmarking**
- Compare departments across multiple metrics
- Identify best and worst performers
- Track sentiment distribution by department
- Visualize performance gaps

### 🧠 **AI-Powered Insights**
- Automatic insight generation from data patterns
- Volume, rating, sentiment, and department insights
- Trend detection and anomaly identification
- Executive-ready narrative summaries

### 🎨 **Modern UI/UX**
- **Dark Glassmorphism Theme** - Premium SaaS-style design
- **Interactive Filters** - Search, department, sentiment, priority filters
- **Responsive Cards** - Hover effects, smooth animations
- **Real-time Updates** - Dynamic filtering and state management
- **Expand/Collapse Controls** - Manage large datasets efficiently

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd patient-satisfaction-platform
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download NLTK data** (first-time setup)
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open in browser**
```
http://localhost:8501
```

---

## 📁 Project Structure

```
patient-satisfaction-platform/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── assets/
│   └── style.css                   # Glassmorphism theme & custom CSS
│
├── modules/                        # Core analytics modules
│   ├── data_loader.py              # CSV/PDF data loading
│   ├── data_validator.py           # Healthcare-specific validation
│   ├── data_cleaner.py             # Data cleaning & normalization
│   ├── preprocessor.py             # Text preprocessing (NLP)
│   ├── feature_engineer.py         # Feature extraction
│   ├── sentiment.py                # VADER sentiment analysis
│   ├── issue_categorizer.py        # Issue classification
│   ├── priority_scorer.py          # Priority scoring algorithm
│   ├── action_mapper.py            # Action recommendation mapping
│   ├── recommender.py              # Department-specific recommendations
│   ├── summarizer.py               # Text summarization (LSA)
│   ├── insight_generator.py        # AI insight generation
│   ├── eda.py                      # Exploratory data analysis
│   └── benchmarking.py             # Department benchmarking
│
├── utils/
│   ├── config.py                   # Configuration constants
│   ├── helpers.py                  # Utility functions
│   └── logger.py                   # Logging setup
│
├── data/
│   ├── raw/                        # Raw uploaded datasets
│   │   └── sample_data.csv         # Sample patient survey data
│   └── processed/                  # Processed outputs
│       ├── processed_data.csv      # Cleaned & enriched data
│       └── insight_report.txt      # Generated insights
│
├── logs/
│   └── app.log                     # Application logs
│
└── notebooks/
    └── eda.ipynb                   # Jupyter notebook for exploration
```

---

## 📊 Data Requirements

### Required CSV Columns
Your patient satisfaction survey CSV should include:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `patient_id` | String/Int | Unique patient identifier | P001, 12345 |
| `department` | String | Hospital department/ward | Emergency, Cardiology |
| `feedback_text` | String | Patient comments/feedback | "The staff was very helpful..." |
| `overall_rating` | Numeric | Satisfaction rating (1-5) | 4, 3.5 |
| `date` | Date | Survey submission date | 2024-01-15 |

### Flexible Column Names
The platform accepts variations:
- **ID**: `patient_id`, `id`, `respondent_id`, `survey_id`
- **Department**: `department`, `dept`, `ward`, `unit`
- **Feedback**: `feedback_text`, `comments`, `feedback`, `review`
- **Rating**: `overall_rating`, `rating`, `satisfaction_score`, `score`

### Healthcare Validation
The system validates datasets to ensure they contain patient satisfaction data by checking for:
- Minimum 3 healthcare-related keywords (patient, doctor, nurse, hospital, etc.)
- Minimum 2 healthcare-related column names
- At least 5 survey responses

---

## 🎯 Usage Guide

### 1. Upload Data
- Navigate to **📤 Upload & Overview**
- Choose **Analyze CSV** or **Analyze PDF**
- Upload your patient satisfaction survey file
- System validates and processes automatically

### 2. Explore Analytics
Use the sidebar to navigate through:

#### 🔍 **EDA (Exploratory Data Analysis)**
- Dataset overview with KPIs
- Rating distribution histograms
- Department performance comparison
- Radar charts for multi-category ratings
- Correlation heatmaps
- Word clouds from feedback
- Trend analysis over time

#### 💬 **Sentiment Analysis**
- Sentiment distribution (Positive/Neutral/Negative)
- VADER compound score distribution
- Sentiment breakdown by department
- Sample feedback with sentiment labels

#### 🏷️ **Issue Categories**
- Issue category distribution
- Category breakdown by department
- Heatmap of issues across departments

#### 🏆 **Department Benchmarking**
- Comparative performance metrics
- Best vs. worst performing departments
- Department-level sentiment analysis
- Rating comparisons

#### ⚡ **Priority Scoring**
- Priority distribution (Critical/High/Medium/Low)
- Priority score histogram
- Average priority by department
- Top 20 critical cases requiring immediate attention

#### 🗺️ **Action Mapper**
- Recommended actions per priority level
- Action distribution visualization
- Actionable insights per case

#### 💡 **Recommendations**
- Department-specific recommendations
- Data-driven improvement suggestions
- NPS-based loyalty insights
- Service recovery priorities

#### 📝 **Feedback Summary**
- **Interactive Filters**: Search keywords, filter by department, sentiment, priority
- **Smart Insights**: % Positive, % Negative, Top Issue per department
- **Sentiment Indicators**: Color-coded borders (green/red/blue)
- **Expand/Collapse Controls**: Manage all summaries at once
- **Automated Summaries**: AI-generated department summaries with deduplication

#### 🧠 **AI Insights**
- Automated insight generation
- Volume, rating, sentiment insights
- Department performance insights
- Executive narrative summary

#### 📊 **Executive Dashboard**
- High-level KPIs
- Key trends and patterns
- Critical alerts
- Actionable recommendations

---

## 🛠️ Technology Stack

### Core Framework
- **Streamlit** - Web application framework
- **Python 3.8+** - Programming language

### Data Processing
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing

### Visualization
- **Plotly** - Interactive charts and graphs
- **Matplotlib** - Static visualizations
- **Seaborn** - Statistical data visualization
- **WordCloud** - Text visualization

### NLP & Machine Learning
- **VADER Sentiment** - Sentiment analysis
- **NLTK** - Natural language processing
- **Sumy** - Text summarization (LSA algorithm)
- **scikit-learn** - Machine learning utilities

### Additional Tools
- **pdfplumber** - PDF text extraction
- **Jupyter** - Notebook environment for exploration

---

## 🎨 Design System

### Glassmorphism Theme
- **Background**: Dark gradient (navy → purple)
- **Cards**: Frosted glass effect with backdrop blur
- **Borders**: Subtle glow with soft shadows
- **Colors**: 
  - Primary: `#6366f1` (Indigo)
  - Secondary: `#8b5cf6` (Purple)
  - Accent: `#a855f7` (Bright Purple)
  - Success: `#2ecc71` (Green)
  - Warning: `#f39c12` (Orange)
  - Danger: `#e74c3c` (Red)

### Typography
- **Headings**: Space Grotesk (Bold, Modern)
- **Body**: DM Sans (Clean, Readable)
- **Monospace**: For data tables and code

### Animations
- Smooth transitions (0.3s cubic-bezier)
- Hover lift effects
- Pulse animations for logos
- Gradient glow effects

---

## 📈 Analytics Algorithms

### Priority Scoring Formula
```python
Priority Score = (
    (6 - rating) * 1.5 +                    # Inverted rating
    ((-vader_compound + 1) / 2) * 3 +       # Negative sentiment
    (word_count / max_word_count) * 1.5 +   # Feedback length
    (is_critical_category ? 1.5 : 0)        # Critical issue flag
) normalized to [0, 10]
```

### Sentiment Classification
- **Positive**: VADER compound ≥ 0.05
- **Negative**: VADER compound ≤ -0.05
- **Neutral**: -0.05 < compound < 0.05

### NPS Categories (1-5 scale)
- **Promoters**: Rating ≥ 4
- **Passives**: Rating = 3
- **Detractors**: Rating ≤ 2
- **NPS Score**: % Promoters - % Detractors

---

## 🔧 Configuration

Edit `utils/config.py` to customize:

```python
# Priority thresholds
PRIORITY_CRITICAL = 7.0
PRIORITY_HIGH = 5.0
PRIORITY_MEDIUM = 3.0

# Sentiment thresholds
SENTIMENT_POSITIVE_THRESHOLD = 0.05
SENTIMENT_NEGATIVE_THRESHOLD = -0.05

# NPS thresholds
NPS_PROMOTER_MIN = 4
NPS_DETRACTOR_MAX = 2

# Critical issue categories
CRITICAL_CATEGORIES = ["Treatment Quality", "Billing", "Cleanliness"]
```

---

## 📝 Sample Data

A sample dataset is included in `data/raw/sample_data.csv` with the following structure:

```csv
patient_id,department,feedback_text,overall_rating,date
P001,Emergency,"Quick service but long wait time",3,2024-01-15
P002,Cardiology,"Excellent care from nursing staff",5,2024-01-16
P003,Orthopedics,"Billing was confusing and unclear",2,2024-01-17
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**HCL Internship Project**  
Patient Satisfaction Analytics Platform

---

## 🙏 Acknowledgments

- **Streamlit** - For the amazing web framework
- **VADER Sentiment** - For robust sentiment analysis
- **Plotly** - For interactive visualizations
- **HCL Technologies** - For the internship opportunity

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the development team

---

## 🗺️ Roadmap

### Upcoming Features
- [ ] PDF report generation
- [ ] Email alert system for critical cases
- [ ] Multi-language support
- [ ] Advanced ML models (BERT, transformers)
- [ ] Real-time data streaming
- [ ] API integration for external systems
- [ ] Mobile-responsive design enhancements
- [ ] Role-based access control
- [ ] Historical trend comparison
- [ ] Predictive analytics

---

**Built with ❤️ for better patient care**