import os
import json
import joblib
import pandas as pd
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "eduguard_model.joblib")
METRICS_PATH = os.path.join(os.path.dirname(__file__), "models", "model_metrics.json")

def load_model():
    if not os.path.exists(MODEL_PATH):
        from train_model import train_and_evaluate
        model, _ = train_and_evaluate()
        return model
    return joblib.load(MODEL_PATH)

def load_metrics():
    if not os.path.exists(METRICS_PATH):
        from train_model import train_and_evaluate
        _, metrics = train_and_evaluate()
        return metrics
    with open(METRICS_PATH, "r") as f:
        return json.load(f)

def predict_student_risk(student_dict):
    """
    Takes a single student dict or DataFrame row and returns predicted probability & risk level.
    """
    model = load_model()
    
    # Ensure correct structure for model pipeline input
    input_df = pd.DataFrame([student_dict])
    
    proba = float(model.predict_proba(input_df)[0, 1])
    
    if proba >= 0.60:
        level = "High"
    elif proba >= 0.35:
        level = "Medium"
    else:
        level = "Low"
        
    return {
        "risk_probability": round(proba, 4),
        "risk_level": level
    }

def explain_student_risk(student_dict):
    """
    Generates data-grounded, human-understandable explanation factors for an individual student prediction.
    Does not invent causes; only uses empirical metrics present in student_dict.
    """
    factors = []
    
    att = float(student_dict.get('attendance_rate', 100))
    if att < 75.0:
        factors.append(f"Attendance rate is critically low at {att}% (below institutional target of 75%).")
    elif att < 85.0:
        factors.append(f"Attendance rate has dropped to {att}%, indicating declining class participation.")

    gpa = float(student_dict.get('gpa', 4.0))
    gpa_change = float(student_dict.get('gpa_change', 0.0))
    if gpa < 2.0:
        factors.append(f"Current Cumulative GPA is {gpa} (Academic Probation Risk).")
    elif gpa < 2.5:
        factors.append(f"Current GPA is {gpa}, showing weak academic standing.")
        
    if gpa_change < -0.3:
        factors.append(f"Academic trajectory declined by {abs(gpa_change):.2f} GPA points from previous semester.")

    assign_rate = float(student_dict.get('assignment_completion_rate', 100))
    late_count = int(student_dict.get('late_submissions_count', 0))
    if assign_rate < 80.0:
        factors.append(f"Assignment completion rate stands at {assign_rate}% (several key submissions missing).")
    if late_count >= 3:
        factors.append(f"Recorded {late_count} late assignment submissions over recent months.")

    failed = int(student_dict.get('failed_courses_count', 0))
    if failed > 0:
        factors.append(f"Student has failed {failed} course{'s' if failed > 1 else ''} in recent term.")

    tuition = int(student_dict.get('tuition_fee_delinquent', 0))
    aid_status = str(student_dict.get('financial_aid_status', 'No Aid'))
    if tuition == 1:
        factors.append("Tuition fee payment is currently delinquent or overdue.")
    if aid_status == "Aid Suspended":
        factors.append("Financial aid status is listed as 'Aid Suspended', requiring administrative follow-up.")

    lib_visits = int(student_dict.get('library_visits_monthly', 10))
    lms_logins = int(student_dict.get('lms_login_frequency_weekly', 10))
    if lib_visits <= 2:
        factors.append(f"Low library usage ({lib_visits} visits/month), indicating low campus resource utilization.")
    if lms_logins <= 3:
        factors.append(f"Low LMS online activity ({lms_logins} logins/week), suggesting potential disengagement.")

    if not factors:
        factors.append("Student demonstrates stable attendance, good academic standing, and consistent engagement.")

    return factors

def get_recommended_interventions(student_dict, factors):
    """
    Formulates evidence-backed recommended support actions based on identified risk factors.
    """
    recommendations = []
    
    att = float(student_dict.get('attendance_rate', 100))
    gpa = float(student_dict.get('gpa', 4.0))
    assign_rate = float(student_dict.get('assignment_completion_rate', 100))
    late_count = int(student_dict.get('late_submissions_count', 0))
    tuition = int(student_dict.get('tuition_fee_delinquent', 0))
    aid_status = str(student_dict.get('financial_aid_status', 'No Aid'))
    failed = int(student_dict.get('failed_courses_count', 0))

    if att < 80.0:
        recommendations.append({
            "category": "Attendance counselling",
            "title": "Schedule Supportive Attendance Counselling",
            "description": "Arrange a 1-on-1 session with department counsellor to understand commute, health, or scheduling difficulties."
        })

    if gpa < 2.5 or failed > 0:
        recommendations.append({
            "category": "Academic mentoring",
            "title": "Assign Academic Mentor & Subject Peer Tutor",
            "description": "Pair student with a senior peer tutor for course-specific doubt clearing and exam preparation strategies."
        })

    if assign_rate < 85.0 or late_count >= 2:
        recommendations.append({
            "category": "Assignment support",
            "title": "Assignment & Time Management Framework",
            "description": "Provide a weekly task checklist, deadline reminders, and short extension grant if medically justified."
        })

    if tuition == 1 or aid_status in ["Aid Suspended", "Pending Application"]:
        recommendations.append({
            "category": "Financial aid referral",
            "title": "Refer to Financial Aid & Student Welfare Service",
            "description": "Connect student with financial aid officers for emergency bursary options, work-study programs, or fee payment plans."
        })

    if len(recommendations) < 2:
        recommendations.append({
            "category": "General student support",
            "title": "Routine Academic Check-in",
            "description": "Conduct a routine 15-minute check-in to affirm progress and provide encouragement."
        })

    return recommendations

def get_model_insights():
    """
    Returns global feature importance and model evaluation metrics for the Risk Analysis page.
    """
    metrics = load_metrics()
    
    # Clean up feature importance names for clean display
    raw_importances = metrics.get("feature_importances", {})
    cleaned_importances = {}
    
    display_names = {
        "attendance_rate": "Attendance Rate (%)",
        "gpa": "Current GPA",
        "gpa_change": "GPA Trajectory Delta",
        "previous_gpa": "Previous Semester GPA",
        "assignment_completion_rate": "Assignment Completion Rate (%)",
        "late_submissions_count": "Late Submissions Count",
        "failed_courses_count": "Failed Courses Count",
        "tuition_fee_delinquent": "Tuition Fee Delinquency",
        "library_visits_monthly": "Monthly Library Visits",
        "lms_login_frequency_weekly": "Weekly LMS Logins",
        "semester": "Semester",
        "financial_aid_status_Aid Suspended": "Financial Aid: Suspended",
        "financial_aid_status_Pending Application": "Financial Aid: Pending",
        "financial_aid_status_Receiving Aid": "Financial Aid: Active Aid",
        "financial_aid_status_No Aid": "Financial Aid: No Aid",
        "department_Computer Science": "Dept: Computer Science",
        "department_Business Administration": "Dept: Business Admin",
        "department_Electrical Engineering": "Dept: Electrical Eng",
        "department_Mechanical Engineering": "Dept: Mechanical Eng",
        "department_Data Science": "Dept: Data Science",
        "department_Humanities & Social Sciences": "Dept: Humanities"
    }

    for feat, val in raw_importances.items():
        name = display_names.get(feat, feat)
        cleaned_importances[name] = val

    # Sort descending
    sorted_importances = dict(sorted(cleaned_importances.items(), key=lambda x: x[1], reverse=True))

    return {
        "metrics": metrics,
        "feature_importances": sorted_importances
    }
