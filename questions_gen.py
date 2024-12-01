import streamlit as st
import pandas as pd
import spacy
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
@st.cache_resource
def load_dataset():
    file_path = 'Software Questions.csv'
    dataset = pd.read_csv(file_path, encoding='latin1')
    return dataset[['Question', 'Category', 'Difficulty']]

dataset = load_dataset()

# Load NLP model
@st.cache_resource
def load_nlp_model():
    return spacy.load("en_core_web_sm")

nlp = load_nlp_model()

# Function to extract keywords from CV (for analysis)
def extract_keywords(cv_text):
    doc = nlp(cv_text)
    keywords = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
    return keywords

# Function to recommend questions based on CV keywords (randomized and extended)
def recommend_questions(cv_keywords, dataset, num_questions=20):
    vectorizer = TfidfVectorizer()
    question_vectors = vectorizer.fit_transform(dataset['Question'])
    cv_vector = vectorizer.transform([' '.join(cv_keywords)])
    similarities = cosine_similarity(cv_vector, question_vectors).flatten()
    dataset['Similarity'] = similarities

    # Get the top 'num_questions' relevant questions sorted by similarity
    recommended = dataset.sort_values(by='Similarity', ascending=False).head(num_questions)

    # Remove duplicates based on the question text
    recommended = recommended.drop_duplicates(subset='Question')
    
    # Ensure the final list has at least 'num_questions' (between 10 and 20)
    additional_questions_needed = max(0, num_questions - len(recommended))  # How many more questions to add
    if additional_questions_needed > 0:
        random_questions = dataset.sample(n=additional_questions_needed, replace=True)
        recommended = pd.concat([recommended, random_questions]).drop_duplicates(subset='Question')

    # Reset index and return the top recommended questions
    recommended = recommended.reset_index(drop=True)  # Remove the index column
    return recommended[['Question', 'Category', 'Difficulty']]

# Streamlit UI
st.title("🎯 Personalized Developer Interview Test Generator")
st.markdown("""
- Upload your CV to generate a **tailored list of interview questions**.  
- The tool analyzes the CV and provide you with **randomly selected relevant questions** based on your profile.
- Please refer to the sidebar for more information and tips.
""")

# File uploader
uploaded_file = st.file_uploader("📄 Upload Your CV (PDF or TXT format)", type=["pdf", "txt"])

if uploaded_file:
    # Read uploaded file
    if uploaded_file.type == "application/pdf":
        import PyPDF2
        reader = PyPDF2.PdfReader(uploaded_file)
        cv_text = " ".join(page.extract_text() for page in reader.pages)
    elif uploaded_file.type == "text/plain":
        cv_text = uploaded_file.read().decode("utf-8")

    # Extract keywords (for analysis, not to display)
    cv_keywords = extract_keywords(cv_text)

    # Recommend 10-20 random questions
    num_questions = random.randint(20, 30)  # Random number between 10 and 20
    recommended_questions = recommend_questions(cv_keywords, dataset, num_questions)

    # Display questions in a clean table format
    st.markdown("### 🧑‍💻 Recommended Interview Questions")
    st.table(recommended_questions[["Question", "Category", "Difficulty"]])

    # Option to download the results
    st.download_button(
        label="📥 Download Questions as CSV",
        data=recommended_questions.to_csv(index=False),
        file_name="interview_questions.csv",
        mime="text/csv"
    )

else:
    st.info("Upload a CV to generate personalized questions.")

st.markdown("""---""")
st.write("""
### Portfolio
For more projects and insights, please visit my [portfolio](https://kimnguyen2002.github.io/Portfolio/).

### Code Repository
You can find the complete code for this application in my GitHub repository [here](https://github.com/kimnguyen2002/Interview-Personalizer).
""")
st.sidebar.markdown("""
 ### Why use this tool?
- **Completely personalized**: Questions are selected based on keywords extracted from your CV.
- **Balanced and fair**: Helps candidates showcase their strengths while avoiding irrelevant or biased questions.

### Please note:
This tool is more well-suited for **software engineer** roles because it is based on the [Software Questions dataset](https://www.kaggle.com/datasets/syedmharis/software-engineering-interview-questions-dataset). But it could be well used for other technical roles.                   
""")
