# ==========================================
# main.py
# FULL BACKEND FOR LOVABLE FRONTEND
# Final Improved Version
# ==========================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import random

# -----------------------------------
# FastAPI App
# -----------------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# Load Saved Model Files
# -----------------------------------

type_model = joblib.load("type_model.pkl")
tfidf_type = joblib.load("vectorizer.pkl")

# -----------------------------------
# Request Schema
# -----------------------------------

class TicketRequest(BaseModel):
    text: str

# -----------------------------------
# Priority Logic
# -----------------------------------

def smart_priority(text):

    text = text.lower()

    high_words = [
        "urgent", "outage", "down", "cannot login",
        "failed", "critical", "error", "hacked",
        "not working", "dringend", "high priority"
    ]

    low_words = [
        "install", "upgrade", "comparison",
        "specification", "request", "billing",
        "payment", "invoice", "refund"
    ]

    if any(word in text for word in high_words):
        return "High"

    elif any(word in text for word in low_words):
        return "Low"

    else:
        return "Medium"

# -----------------------------------
# Hybrid Type Prediction
# -----------------------------------

def predict_ticket_type(ticket):

    text = ticket.lower()

    service_words = [
        "billing", "payment", "invoice",
        "refund", "order", "comparison",
        "pricing", "purchase", "specification",
        "subscription", "renewal", "license"
    ]

    if any(word in text for word in service_words):
        return 0, 95.0

    vec = tfidf_type.transform([ticket])

    pred = type_model.predict(vec)[0]

    score = type_model.decision_function(vec)[0]
    confidence = 1 / (1 + np.exp(-abs(score)))
    confidence = round(confidence * 100, 2)

    return pred, confidence

# -----------------------------------
# Routing Logic
# -----------------------------------

def route_ticket(ticket_type, priority, ticket, confidence):

    text = ticket.lower()

    if "billing" in text or "payment" in text or "refund" in text:
        return "Billing Support Team"

    if "comparison" in text or "pricing" in text or "purchase" in text:
        return "Sales Support Team"

    if confidence < 65:
        return "Manual Review Queue"

    if ticket_type == 1 and priority == "High":
        return "IT Escalation Team"

    elif ticket_type == 1 and priority == "Medium":
        return "Technical Support Team"

    elif ticket_type == 1 and priority == "Low":
        return "General IT Helpdesk"

    elif ticket_type == 0 and priority == "High":
        return "Service Desk Priority Queue"

    elif ticket_type == 0 and priority == "Medium":
        return "Service Request Team"

    else:
        return "General Helpdesk Queue"

# -----------------------------------
# SLA Logic
# -----------------------------------

def get_sla(priority):

    if priority == "High":
        return "Within 1 Hour"

    elif priority == "Medium":
        return "Within 4 Hours"

    else:
        return "Within 24 Hours"

# -----------------------------------
# Suggested Reply
# -----------------------------------

def suggested_reply(ticket_type, priority, route):

    if ticket_type == "Technical Issue":
        return f"Your issue has been assigned to the {route}. Our team will investigate and respond {get_sla(priority).lower()}."

    elif ticket_type == "Service Request":
        return f"Your request has been forwarded to the {route}. We will get back to you {get_sla(priority).lower()}."

    else:
        return "Please enter a detailed support issue or request."

# -----------------------------------
# Home Route
# -----------------------------------

@app.get("/")
def home():
    return {"message": "Customer Ticket Triage API Running"}

# -----------------------------------
# Predict Route
# -----------------------------------

@app.post("/predict")
def predict(data: TicketRequest):

    ticket = data.text.strip()
    text_clean = ticket.lower()

    # -----------------------------------
    # Invalid Input Detection
    # -----------------------------------

    casual_words = [
        "hi", "hello", "thanks", "thank you",
        "bye", "ok", "okay", "good morning"
    ]

    if len(ticket.split()) < 4 or text_clean in casual_words:
        return {
            "ticket_id": "N/A",
            "ticket_type": "Invalid Input",
            "confidence": 0,
            "priority": "-",
            "route_to": "Manual Review",
            "sla": "-",
            "reply": "Please enter a detailed support issue or request."
        }

    # -----------------------------------
    # Normal Prediction
    # -----------------------------------

    pred, confidence = predict_ticket_type(ticket)

    ticket_type = "Technical Issue" if pred == 1 else "Service Request"

    priority = smart_priority(ticket)

    route = route_ticket(pred, priority, ticket, confidence)

    sla = get_sla(priority)

    reply = suggested_reply(ticket_type, priority, route)

    ticket_id = "TKT-" + str(random.randint(10000, 99999))

    return {
        "ticket_id": ticket_id,
        "ticket_type": ticket_type,
        "confidence": confidence,
        "priority": priority,
        "route_to": route,
        "sla": sla,
        "reply": reply
    }
