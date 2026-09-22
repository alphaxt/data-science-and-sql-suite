# 📧 Email Spam Detection Project – Task 4

## Project Outline

This project focuses on building an intelligent system to classify messages as either Spam or Ham using Natural Language Processing (NLP) and Machine Learning.

## 1. Objective

- Detect spam messages automatically.
- Apply text preprocessing techniques to clean and prepare the data.
- Train a machine learning model to classify new messages.
- Deploy a simple prediction app using Streamlit.

## 2. Dataset

- Source: SMS Spam Collection Dataset
- Contains labeled SMS messages
- Classes:
  - Ham (Not Spam)
  - Spam

## 3. Workflow

1. Load the dataset
2. Clean the data
   - remove unnecessary columns
   - rename columns
   - handle missing values and duplicates
3. Explore the data
   - check class distribution
   - analyze message length and word patterns
4. Preprocess text
   - lowercase text
   - remove punctuation and special characters
   - tokenize words
   - remove stopwords
   - apply stemming
5. Convert text into features
   - use TF-IDF vectorization
6. Train the model
   - use Multinomial Naive Bayes
7. Evaluate performance
   - accuracy
   - precision
   - recall
   - F1-score
   - confusion matrix
8. Build a prediction app
   - create a Streamlit interface for real-time testing

## 4. Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- NLTK
- Matplotlib
- Seaborn
- Streamlit
- Jupyter Notebook

## 5. Project Structure

- Email_Spam_Detection.ipynb — main notebook for analysis and modeling
- app/app.py — Streamlit web app
- app/requirements.txt — Python dependencies
- dataset/spam.csv — dataset file
- outputs/ — saved model metrics and reports

## 6. How to Run

```bash
cd DataScience-Task4-EmailSpamDetection
pip install -r app/requirements.txt
streamlit run app/app.py
```

## 7. Expected Outcome

- The model should classify incoming messages as spam or ham.
- The web app should provide a quick and interactive prediction experience.
