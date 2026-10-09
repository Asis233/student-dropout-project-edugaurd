import os
import random
import numpy as np
import pandas as pd

def generate_student_dataset(n_samples=600, random_seed=42):
    """
    Generates a realistic synthetic dataset for student dropout early warning prediction.
    Features reflect academic, attendance, assignment, library, and financial indicators.
    """
    np.random.seed(random_seed)
    random.seed(random_seed)

    departments = [
        "Computer Science",
        "Business Administration",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Data Science",
        "Humanities & Social Sciences"
    ]

    first_names = [
        "Aarav", "Ananya", "Rohan", "Priya", "Rahul", "Neha", "Vikram", "Sneha",
        "Aditya", "Kavya", "Arjun", "Isha", "Siddharth", "Pooja", "Amit", "Riya",
        "Karan", "Tanvi", "Dev", "Meera", "Yash", "Divya", "Alex", "Jordan",
        "Taylor", "Morgan", "Sam", "Chris", "Pat", "Riley", "Casey", "Avery"
    ]

    last_names = [
        "Sharma", "Verma", "Patel", "Singh", "Kumar", "Gupta", "Reddy", "Nair",
        "Joshi", "Mehta", "Rao", "Chowdhury", "Deshmukh", "Iyer", "Banerjee", "Kulkarni",
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"
    ]

    financial_aid_options = ["Receiving Aid", "No Aid", "Pending Application", "Aid Suspended"]
    financial_aid_weights = [0.45, 0.40, 0.10, 0.05]

    students = []
    start_id = 101

    for i in range(n_samples):
        student_id = f"EDU-2026-{start_id + i:03d}"
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        dept = random.choice(departments)
        semester = random.randint(1, 8)

        # Baseline student profile latent factor (0 = high performing, 1 = struggling)
        latent_struggle = np.random.beta(a=1.5, b=3.5)

        # Attendance: correlated with struggle
        attendance_base = 95.0 - (latent_struggle * 45.0) + np.random.normal(0, 4.0)
        attendance_rate = float(np.clip(attendance_base, 42.0, 99.5))

        # GPA: correlated with struggle
        gpa_base = 3.8 - (latent_struggle * 2.2) + np.random.normal(0, 0.25)
        gpa = float(np.clip(gpa_base, 1.1, 4.0))

        # Previous GPA
        previous_gpa_base = gpa + (latent_struggle * np.random.uniform(-0.4, 0.5))
        previous_gpa = float(np.clip(previous_gpa_base, 1.2, 4.0))
        gpa_change = round(gpa - previous_gpa, 2)

        # Assignment completion rate
        assign_base = 98.0 - (latent_struggle * 50.0) + np.random.normal(0, 5.0)
        assignment_completion_rate = float(np.clip(assign_base, 35.0, 100.0))

        # Late submissions
        late_submissions_count = int(np.clip(np.random.poisson(latent_struggle * 4.5), 0, 9))

        # Library visits & LMS logins
        library_visits_monthly = int(np.clip(np.random.poisson((1 - latent_struggle) * 14.0 + 1.0), 0, 30))
        lms_login_frequency_weekly = int(np.clip(np.random.poisson((1 - latent_struggle) * 12.0 + 2.0), 1, 25))

        # Financial status
        financial_aid_status = np.random.choice(financial_aid_options, p=financial_aid_weights)
        if latent_struggle > 0.65 and financial_aid_status == "Aid Suspended":
            tuition_fee_delinquent = np.random.choice([0, 1], p=[0.2, 0.8])
        elif latent_struggle > 0.5:
            tuition_fee_delinquent = np.random.choice([0, 1], p=[0.7, 0.3])
        else:
            tuition_fee_delinquent = np.random.choice([0, 1], p=[0.95, 0.05])

        # Failed courses count
        if latent_struggle > 0.6:
            failed_courses_count = int(np.random.choice([0, 1, 2, 3], p=[0.3, 0.4, 0.2, 0.1]))
        elif latent_struggle > 0.4:
            failed_courses_count = int(np.random.choice([0, 1, 2], p=[0.7, 0.25, 0.05]))
        else:
            failed_courses_count = 0

        # Ground truth dropout target (1 = dropped out / high risk outcome, 0 = retained)
        # Logit equation combining indicators with realistic threshold
        risk_score = (
            (85.0 - attendance_rate) * 0.08 +
            (3.0 - gpa) * 1.5 +
            (max(0, -gpa_change)) * 1.2 +
            (90.0 - assignment_completion_rate) * 0.05 +
            late_submissions_count * 0.4 +
            failed_courses_count * 1.1 +
            tuition_fee_delinquent * 1.2 +
            (1 if financial_aid_status == "Aid Suspended" else 0) * 0.8 -
            (library_visits_monthly * 0.06) -
            (lms_login_frequency_weekly * 0.05)
        )
        # Convert risk score to probability via sigmoid + noise
        prob = 1.0 / (1.0 + np.exp(-(risk_score - 2.2)))
        dropout_target = int(np.random.uniform(0, 1) < prob)

        # Initial risk label for visualization
        if prob > 0.65:
            risk_level = "High"
        elif prob > 0.35:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        students.append({
            "student_id": student_id,
            "name": name,
            "department": dept,
            "semester": semester,
            "attendance_rate": round(attendance_rate, 1),
            "gpa": round(gpa, 2),
            "previous_gpa": round(previous_gpa, 2),
            "gpa_change": round(gpa_change, 2),
            "assignment_completion_rate": round(assignment_completion_rate, 1),
            "late_submissions_count": late_submissions_count,
            "library_visits_monthly": library_visits_monthly,
            "lms_login_frequency_weekly": lms_login_frequency_weekly,
            "financial_aid_status": financial_aid_status,
            "tuition_fee_delinquent": tuition_fee_delinquent,
            "failed_courses_count": failed_courses_count,
            "dropout_target": dropout_target,
            "risk_level": risk_level,
            "risk_probability": round(float(prob), 4),
            "last_follow_up": random.choice(["2026-09-10", "2026-09-22", "2026-10-01", "None", "None", "None"]),
            "counsellor_notes": "Initial risk assessment completed." if risk_level != "Low" else "No issues flagged."
        })

    df = pd.DataFrame(students)
    return df

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = generate_student_dataset(n_samples=650)
    output_path = os.path.join("data", "student_data.csv")
    df.to_csv(output_path, index=False)
    print(f"Generated dataset with {len(df)} records saved to {output_path}")
    print("Class distribution:")
    print(df['dropout_target'].value_counts(normalize=True))
    print("Risk level distribution:")
    print(df['risk_level'].value_counts())
