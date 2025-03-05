import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Download necessary NLTK resources
#nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

def clean_text(text):
    if pd.isna(text):  # Handle NaN values
        return ""
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'http\S+|www\S+', '', text)  # Remove URLs
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'[^a-z\s]', '', text)  # Remove special characters
    tokens = word_tokenize(text)  # Tokenization
    tokens = [word for word in tokens if word not in stopwords.words('english')]  # Remove stopwords
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]  # Stemming
    return ' '.join(tokens)

def preprocess_data(df):
    df = df.drop_duplicates()  # Remove duplicate rows
    df.fillna(df.mean(numeric_only=True), inplace=True)  # Replace NaN with mean for numeric columns
    text_columns = df.select_dtypes(include=['object']).columns  # Identify text columns
    
    for col in text_columns:
        df[col] = df[col].apply(clean_text)  # Apply text cleaning
    
    return df

# Example usage
data = {
    'Text': ["Hello World! Visit http://example.com", "This is a test 123", "Hello world!", np.nan],
    'Numbers': [10, np.nan, 30, 40]
}
df = pd.DataFrame(data)
cleaned_df = preprocess_data(df)
print(cleaned_df)