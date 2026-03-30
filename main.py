import joblib
import os
import sys
from colorama import init, Fore, Style
import database

# Initialize colorama for Windows
init(autoreset=True)

def load_ml_components():
    """Loads the pre-trained vectorizer and model."""
    try:
        vectorizer = joblib.load('vectorizer.pkl')
        model = joblib.load('spam_model.pkl')
        return vectorizer, model
    except FileNotFoundError:
        print(Fore.RED + "[!] Critical Error: ML model files not found.")
        print(Fore.YELLOW + "Ensure 'spam_model.pkl' and 'vectorizer.pkl' are in the root directory.")
        sys.exit(1)

def scan_text(vectorizer, model):
    """Handles the user input and prediction logic."""
    print(Fore.CYAN + "\n--- Text Scanner ---")
    user_text = input("Enter the text message or email content to scan:\n> ")
    
    if not user_text.strip():
        print(Fore.RED + "[!] Error: Input cannot be empty.")
        return

    # Process through the ML pipeline
    vectorized_text = vectorizer.transform([user_text])
    prediction_num = model.predict(vectorized_text)[0]
    probabilities = model.predict_proba(vectorized_text)[0]
    
    # Format results
    confidence = probabilities[prediction_num] * 100
    result = "PHISHING / SPAM" if prediction_num == 1 else "SAFE"
    color = Fore.RED if prediction_num == 1 else Fore.GREEN

    print("\n" + "="*40)
    print(color + f"[*] THREAT ANALYSIS: {result}")
    print(Fore.WHITE + f"[*] CONFIDENCE:    {confidence:.2f}%")
    print("="*40)

    # Log to SQLite
    database.log_scan(user_text, result, confidence)

def view_history():
    """Displays the SQLite scan history."""
    print(Fore.CYAN + "\n--- Recent Scan History ---")
    records = database.get_history()
    
    if not records:
        print(Fore.YELLOW + "No scans found in the database.")
        return
    
    for row in records:
        timestamp, snippet, pred, conf = row
        color = Fore.RED if pred == "PHISHING / SPAM" else Fore.GREEN
        print(f"[{timestamp}] {color}{pred} ({conf:.1f}%){Style.RESET_ALL} | {snippet}")

def main_menu():
    """The continuous CLI loop."""
    database.init_db()
    print(Fore.MAGENTA + "Loading AI Security Core...")
    vectorizer, model = load_ml_components()
    
    while True:
        print(Fore.BLUE + "\n" + "#"*30)
        print(Fore.WHITE + Style.BRIGHT + "  AI PHISHING ANALYZER CLI")
        print(Fore.BLUE + "#"*30)
        print("1. Scan New Text")
        print("2. View Scan History")
        print("3. Exit System")
        
        choice = input(Fore.YELLOW + "\nEnter choice [1-3]: " + Style.RESET_ALL)
        
        if choice == '1':
            scan_text(vectorizer, model)
        elif choice == '2':
            view_history()
        elif choice == '3':
            print(Fore.CYAN + "Shutting down AI Core. Goodbye.")
            sys.exit(0)
        else:
            print(Fore.RED + "[!] Invalid input. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()