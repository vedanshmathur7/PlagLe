import PyPDF2
import docx
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import mysql.connector

# Ensure stopwords are downloaded locally
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords', quiet=True)

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + " "
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return " ".join([paragraph.text for paragraph in doc.paragraphs])

def preprocess_text(text):
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    
    # 3. Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    cleaned_words = [word for word in words if word not in stop_words]
    
    return " ".join(cleaned_words)

def calculate_similarity(text1, text2):
    # Prevent empty vocabulary errors
    if not text1 or not text2:
        return 0.0
        
    vectorizer = TfidfVectorizer()
    # Create vectors
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    
    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    return float(similarity_matrix[0][0])

def insert_similarity_score(db_connection, doc1_id, doc2_id, algorithm_id, score):
    cursor = db_connection.cursor()
    
    # Enforce strictly doc1_id < doc2_id as per Step 1 Database rules
    if doc1_id > doc2_id:
        doc1_id, doc2_id = doc2_id, doc1_id
        
    query = """
    INSERT INTO Similarity (doc1_id, doc2_id, algorithm_id, score)
    VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (doc1_id, doc2_id, algorithm_id, score))
        db_connection.commit()
        print(f"Successfully inserted Similarity Score: {score:.4f} for Docs ({doc1_id}, {doc2_id})")
    except mysql.connector.Error as err:
        print(f"Database insertion failed: {err}")

# Helper utility to easily test
def test_comparison_files(file1_path, file2_path):
    print(f"Comparing '{file1_path}' against '{file2_path}'...")
    
    # Simple extension detection
    def extract(path):
        if path.endswith('.pdf'): return extract_text_from_pdf(path)
        elif path.endswith('.docx'): return extract_text_from_docx(path)
        else: return extract_text_from_txt(path)
        
    try:
        text1 = extract(file1_path)
        text2 = extract(file2_path)
        
        cleaned1 = preprocess_text(text1)
        cleaned2 = preprocess_text(text2)
        
        score = calculate_similarity(cleaned1, cleaned2)
        print(f"-----\nSimilarity Score: {score:.4f}\n-----")
        return score
    except Exception as e:
        print(f"Error during comparison: {e}")
        return 0.0
