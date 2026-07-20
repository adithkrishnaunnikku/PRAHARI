import random
import uuid

from app.core.database import SessionLocal
from app.models.incident import IncidentEvent
from app.models.audit import AuditLog


db = SessionLocal()


# ----------------------------
# Sample Data by ivan
# ----------------------------

citizens = [
    "Rahul Sharma",
    "Priya Nair",
    "Aman Gupta",
    "Sneha Reddy",
    "Arjun Menon",
    "Rohan Das",
    "Neha Singh",
    "Karan Patel"
]

locations = [
    "Mumbai",
    "Delhi",
    "Bengaluru",
    "Chennai",
    "Hyderabad",
    "Kochi",
    "Pune",
    "Ahmedabad"
]

fraud_types = [
    "UPI Fraud",
    "OTP Scam",
    "Investment Scam",
    "Courier Scam",
    "Identity Theft",
    "Loan Scam"
]

risk_levels = [
    "LOW",
    "MEDIUM",
    "HIGH"
]

statuses = [
    "OPEN",
    "UNDER_REVIEW",
    "CLOSED"
]


# ----------------------------
# Create Incidents
# ----------------------------

for i in range(10):

    incident = IncidentEvent(
        incident_id=str(uuid.uuid4())[:8],
        citizen_name=random.choice(citizens),
        phone_number=f"98{random.randint(10000000,99999999)}",
        transcript=f"Sample fraud complaint #{i+1}",
        location=random.choice(locations),
        fraud_type=random.choice(fraud_types),
        risk_level=random.choice(risk_levels),
        status=random.choice(statuses)
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    audit = AuditLog(
        incident_id=incident.incident_id,
        action="INCIDENT_CREATED",
        rule_hits={
            "keyword_match": True,
            "upi_detected": random.choice([True, False]),
            "otp_detected": random.choice([True, False])
        },
        model_version="v1.0",
        prompt_version="v1",
        score_components={
            "keyword_score": random.randint(20,40),
            "llm_score": random.randint(30,60),
            "risk_score": random.randint(40,90)
        },
        threshold_version="v1"
    )

    db.add(audit)
    db.commit()

print("Successfully inserted sample incidents and audit logs!")

db.close()
