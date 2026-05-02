# 🎫 Customer Ticket Triage System

An AI-powered system that automatically classifies customer support tickets, assigns priority, routes them to the correct team, and generates response suggestions using Machine Learning and rule-based logic.

---

## 🚀 Features

- 🔍 Ticket Classification (Technical Issue / Service Request)
- ⚡ Priority Assignment (High, Medium, Low)
- 🧭 Intelligent Routing to Support Teams
- ⏱️ SLA Estimation (Response Time)
- 💬 Automated Suggested Reply
- 📊 Model Evaluation with Accuracy, Confusion Matrix

---

## 🧠 Machine Learning Approach

- **Model Used:** LinearSVC (Support Vector Classifier)
- **Feature Extraction:** TF-IDF Vectorization
- **Classification Type:** Binary Classification

### Why LinearSVC?
- Works well with high-dimensional sparse text data
- Efficient and fast
- Achieved best accuracy (~83.87%)

---

## 📊 Dataset

- ~1400 customer support tickets
- Fields used:
  - Subject
  - Description
  - Ticket Type

### Preprocessing Steps:
- Combined subject + description
- Handled missing values
- Cleaned text data
- Converted labels into binary classes:
  - `1 → Technical Issue`
  - `0 → Service Request`

---

## ⚙️ System Architecture

The system follows a **hybrid approach**:

### 🔹 Machine Learning
- Classifies ticket type

### 🔹 Rule-Based Logic
- Assigns priority
- Routes tickets
- Determines SLA
- Generates response

---

## 🧾 Priority Logic

| Priority | Condition |
|--------|----------|
| High | urgent, outage, error, critical |
| Medium | default |
| Low | billing, request, upgrade |

---

## 🧭 Routing Logic

- Technical + High → IT Escalation Team
- Technical + Medium → Technical Support Team
- Service Request → Service Team
- Billing → Billing Support
- Sales Queries → Sales Team
- Low confidence → Manual Review

---

## ⏱️ SLA (Response Time)

| Priority | SLA |
|---------|-----|
| High | Within 1 Hour |
| Medium | Within 4 Hours |
| Low | Within 24 Hours |

---

## 🛠️ Tech Stack

- Python
- Pandas, NumPy
- Scikit-learn
- TF-IDF Vectorizer
- LinearSVC
- FastAPI
- Joblib

---

## 📈 Model Performance

- Accuracy: **83.87%**
- Precision: ~0.84
- Recall (Technical): ~0.91

---

Website link -> https://customer-ticket-triage-system.lovable.app/
