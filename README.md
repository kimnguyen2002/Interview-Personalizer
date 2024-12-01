# Interview Personalizer
## 🎯 Personalized Developer Interview Test Generator
A web application built with Streamlit that generates personalized interview questions tailored to the skills and experience outlined in a candidate's CV. This tool is designed primarily for software engineers but can be adapted for other technical roles.

Check out the live Streamlit App [here](https://interviewpersonalizer.streamlit.app/). 

## 🚀 Features

- Tailored Questions: Uses NLP techniques to extract keywords from uploaded CVs and recommend relevant questions.
- Randomized Selection: Generates 20–30 questions to ensure a diverse set of interview topics.
- Downloadable Results: Provides an option to download the recommended questions in CSV format.
- Developer-Focused: The dataset is curated specifically for software engineering roles.

## 📋 How It Works

- **Upload Your CV:** Accepts CVs in PDF or TXT format.
- **Keyword Extraction:** Uses the spaCy NLP library to extract relevant keywords from your CV.
- **Question Recommendation:** Matches your skills with questions from a preloaded dataset using TF-IDF and cosine similarity.
- **Results:** Displays a list of recommended interview questions, including their category and difficulty level.
- **Download Option:** Download the questions as a CSV file for future reference.

## 🖥️ Installation and Setup
1. Clone the repository:
```bash
git clone https://github.com/kimnguyen2002/Interview-Personalizer.git
cd Personalized-Interview-Test-Generator
```
2. Install required dependencies:
```bash
pip install -r requirements.txt
```
3. Run the Streamlit app:
```bash
streamlit run app.py
```
## 📂 Project Structure
```
Personalized-Interview-Test-Generator/
├── app.py                     # Main Streamlit app file
├── requirements.txt           # Required Python packages
├── Software Questions.csv     # Dataset containing interview questions
└── README.md                  # Project documentation 
```

## 📊 Dataset Information
The app uses a dataset, **Software Questions.csv**, that contains:
- **Question:** The text of the interview question.
- **Category:** The category/topic of the question (e.g., algorithms, databases).
- **Difficulty:** A difficulty rating (e.g., easy, medium, hard).
Feel free to replace this dataset with your own to adapt the tool for other roles.

## 📜 License
This project is licensed under the MIT License.
