import pandas as pd
import urllib.request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

def main():
    print("[*] Fetching dataset into memory...")
    # Using a reliable raw URL for the standard SMS Spam dataset
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    
    try:
        df = pd.read_csv(url, sep='\t', header=None, names=['label', 'message'])
    except Exception as e:
        print(f"[!] Error downloading dataset: {e}")
        return

    print(f"[*] Loaded {len(df)} text records. Initializing local training...")
    
    # Map labels to binary values (0 = Safe, 1 = Spam/Phishing)
    df['label_num'] = df.label.map({'ham': 0, 'spam': 1})
    X = df.message
    y = df.label_num

    # Initialize TF-IDF Vectorizer
    print("[*] Vectorizing text data...")
    vectorizer = TfidfVectorizer(stop_words='english')
    X_train_dtm = vectorizer.fit_transform(X)

    # Train the Multinomial Naive Bayes Model
    print("[*] Training Multinomial Naive Bayes classifier...")
    nb_model = MultinomialNB()
    nb_model.fit(X_train_dtm, y)

    # Export the architecture (Micro-Model Export)
    print("[*] Serializing model and vectorizer...")
    joblib.dump(nb_model, 'spam_model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')

    print("[+] SUCCESS: spam_model.pkl and vectorizer.pkl generated in root directory.")

if __name__ == "__main__":
    main()