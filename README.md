# Offline AI Phishing & Spam Analyzer CLI

> **An Intelligent, Privacy-First Cybersecurity Tool for Real-Time Threat Detection.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Built for VIT Bhopal](https://img.shields.io/badge/Academic-VIT%20Bhopal-red.svg)](https://vitbhopal.ac.in/)

## Overview

Current phishing detection relies on cloud-based APIs (OpenAI, Google Cloud), which introduces latency and severe privacy risks. This project is a **100% Offline CLI Tool** that utilizes a locally trained Logistic Regression model to classify text as "SAFE" or "PHISHING" with high confidence. It is engineered for low-resource environments and high-security data compliance.

---

## Technical Architecture

The system follows a **Decoupled Micro-Model Architecture**:

1. **Training Pipeline (`train_model.py`):** Fetches the UCI SMS dataset, performs TF-IDF Vectorization, and trains a Logistic Regression model with `class_weight='balanced'` to eliminate false negatives.
2. **Inference Engine (`main.py`):** Loads the serialized `.pkl` files and performs real-time classification on raw user input.
3. **Persistence Layer (`database.py`):** A lightweight SQLite implementation that logs every scan for forensic history.

### File Structure

```
offline-ai-spam-analyzer/
├── main.py                # Primary Entry Point (CLI Loop)
├── database.py            # SQLite Storage Logic
├── train_model.py         # ML Training Script
├── spam_model.pkl         # Serialized AI Model
├── vectorizer.pkl         # Serialized TF-IDF Weights
├── requirements.txt       # Environment Dependencies
└── README.md              # Documentation
```

## Quick Start

### 1. Environment Setup

Clone the repository and initialize a virtual environment to ensure dependency isolation:

```bash
git clone https://github.com/YOUR-USERNAME/offline-ai-spam-analyzer.git
cd offline-ai-spam-analyzer
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch the Application

```bash
python main.py
```

##  Detailed Usage Guide

Once the system launches, you will see a colorized menu. Use the numeric keys to navigate:

**Option 1: Scan New Text**
- **Input:** Paste any suspicious message (e.g., "Click the link to win 1 million dollars!")
- **Process:** The AI Core performs a TF-IDF transformation and calculates a probability score.
- **Output:** Returns a color-coded THREAT ANALYSIS (SAFE or PHISHING) and a CONFIDENCE SCORE.

**Option 2: View Scan History**
- **Input:** Select Option 2.
- **Output:** The system queries the scan_history.db and displays the last 10 scans with precise timestamps.

##  Architectural Decisions

- **Why Logistic Regression?** While Naive Bayes is faster, Logistic Regression with `class_weight='balanced'` was chosen to specifically address the 86/14 class imbalance in the UCI dataset, significantly reducing False Negatives on lottery-based phishing strings.
- **Why TF-IDF?** Unlike simple Bag-of-Words, TF-IDF penalizes common English words and highlights specific threat-signature tokens.

## Troubleshooting

- **ModuleNotFoundError:** Ensure your virtual environment is active (`venv\Scripts\activate`).
- **Access Denied:** Ensure you are running the terminal as an Administrator if SQLite cannot create the .db file.

## Author

Shivansh Prashant  
Student Coordinator | VIT Bhopal University  
Reg No: 25BAI10384  
Major: B.Tech CSE (AI & ML)

Developed for the Fundamentals in AI and ML (CSA2001) BYOP Submission.

---
