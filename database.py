import os
import sqlite3
import pandas as pd
import numpy as np

DB_PATH = os.path.join(os.path.dirname(__file__), "eduguard.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force_reseed=False):
    conn = get_connection()
    cursor = conn.cursor()

    if force_reseed:
        cursor.execute("DROP TABLE IF EXISTS outcomes_tracking")
        cursor.execute("DROP TABLE IF EXISTS interventions")
        cursor.execute("DROP TABLE IF EXISTS students")

    # 1. Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            semester INTEGER NOT NULL,
            attendance_rate REAL NOT NULL,
            gpa REAL NOT NULL,
            previous_gpa REAL NOT NULL,
            gpa_change REAL NOT NULL,
            assignment_completion_rate REAL NOT NULL,
            late_submissions_count INTEGER NOT NULL,
            library_visits_monthly INTEGER NOT NULL,
            lms_login_frequency_weekly INTEGER NOT NULL,
            financial_aid_status TEXT NOT NULL,
            tuition_fee_delinquent INTEGER NOT NULL,
            failed_courses_count INTEGER NOT NULL,
            dropout_target INTEGER DEFAULT 0,
            risk_level TEXT NOT NULL,
            risk_probability REAL NOT NULL,
            last_follow_up TEXT,
            counsellor_notes TEXT
        )
    """)

    # 2. Interventions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interventions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            student_name TEXT NOT NULL,
            intervention_type TEXT NOT NULL,
            assigned_counsellor TEXT NOT NULL,
            creation_date TEXT NOT NULL,
            follow_up_date TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT,
            outcome TEXT,
            FOREIGN KEY (student_id) REFERENCES students (student_id)
        )
    """)

    # 3. Outcomes tracking table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS outcomes_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intervention_id INTEGER,
            student_id TEXT NOT NULL,
            student_name TEXT NOT NULL,
            initial_risk_level TEXT NOT NULL,
            initial_risk_prob REAL NOT NULL,
            intervention_type TEXT NOT NULL,
            intervention_date TEXT NOT NULL,
            follow_up_date TEXT NOT NULL,
            enrollment_status TEXT NOT NULL,
            attendance_change REAL NOT NULL,
            gpa_change REAL NOT NULL,
            academic_progress_status TEXT NOT NULL,
            outcome_notes TEXT,
            FOREIGN KEY (student_id) REFERENCES students (student_id)
        )
    """)

    conn.commit()

    # Seed students if table is empty
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]

    if count == 0:
        csv_path = os.path.join(os.path.dirname(__file__), "data", "student_data.csv")
        if not os.path.exists(csv_path):
            from generate_data import generate_student_dataset
            df = generate_student_dataset(n_samples=650)
            os.makedirs("data", exist_ok=True)
            df.to_csv(csv_path, index=False)
        else:
            df = pd.read_csv(csv_path)

        for _, row in df.iterrows():
            cursor.execute("""
                INSERT OR REPLACE INTO students (
                    student_id, name, department, semester, attendance_rate, gpa,
                    previous_gpa, gpa_change, assignment_completion_rate, late_submissions_count,
                    library_visits_monthly, lms_login_frequency_weekly, financial_aid_status,
                    tuition_fee_delinquent, failed_courses_count, dropout_target, risk_level,
                    risk_probability, last_follow_up, counsellor_notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(row['student_id']), str(row['name']), str(row['department']), int(row['semester']),
                float(row['attendance_rate']), float(row['gpa']), float(row['previous_gpa']), float(row['gpa_change']),
                float(row['assignment_completion_rate']), int(row['late_submissions_count']),
                int(row['library_visits_monthly']), int(row['lms_login_frequency_weekly']),
                str(row['financial_aid_status']), int(row['tuition_fee_delinquent']), int(row['failed_courses_count']),
                int(row['dropout_target']), str(row['risk_level']), float(row['risk_probability']),
                str(row['last_follow_up']), str(row['counsellor_notes'])
            ))

        # Seed realistic interventions for demonstration
        sample_interventions = [
            ("EDU-2026-104", "Rohan Singh", "Academic mentoring", "Dr. Sarah Jenkins", "2026-09-01", "2026-09-15", "Completed", "Assigned peer tutor for Linear Algebra.", "Grade improved from C to B."),
            ("EDU-2026-112", "Priya Sharma", "Attendance counselling", "Prof. Marcus Vance", "2026-09-05", "2026-09-20", "Completed", "Met with student to discuss commute issues.", "Attendance stabilized to 88%."),
            ("EDU-2026-125", "Amit Patel", "Financial aid referral", "Ms. Elena Rostova", "2026-09-10", "2026-10-05", "In Progress", "Submitted work-study program application.", "Pending approval from Dean."),
            ("EDU-2026-138", "Sneha Nair", "Assignment support", "Dr. Sarah Jenkins", "2026-09-12", "2026-10-10", "Follow-Up Required", "Provided extension & assignment checklist.", "1 of 3 late tasks submitted."),
            ("EDU-2026-149", "Dev Kulkarni", "Personal counselling referral", "Mr. David Miller", "2026-09-15", "2026-10-12", "Planned", "Scheduled intake session with Wellness Center.", "Awaiting session date."),
            ("EDU-2026-155", "Tanvi Joshi", "Academic mentoring", "Dr. Sarah Jenkins", "2026-09-18", "2026-10-15", "In Progress", "Weekly check-in for Data Structures course.", "Showing positive engagement.")
        ]

        for s_id, s_name, itype, couns, cdate, fdate, st, nts, out in sample_interventions:
            cursor.execute("""
                INSERT INTO interventions (
                    student_id, student_name, intervention_type, assigned_counsellor,
                    creation_date, follow_up_date, status, notes, outcome
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (s_id, s_name, itype, couns, cdate, fdate, st, nts, out))

        # Seed sample outcome tracking records
        sample_outcomes = [
            (1, "EDU-2026-104", "Rohan Singh", "High", 0.78, "Academic mentoring", "2026-09-01", "2026-09-15", "Enrolled", 6.2, 0.45, "Improved", "Student responded exceptionally well to peer tutoring; GPA increased by 0.45."),
            (2, "EDU-2026-112", "Priya Sharma", "High", 0.82, "Attendance counselling", "2026-09-05", "2026-09-20", "Enrolled", 14.5, 0.20, "Improved", "Transportation obstacle resolved; attendance increased by 14.5%."),
            (3, "EDU-2026-108", "Kavya Iyer", "Medium", 0.52, "Assignment support", "2026-08-25", "2026-09-10", "Enrolled", 4.0, 0.15, "Stable", "Assignment completion rate restored to 90%."),
            (4, "EDU-2026-119", "Aditya Deshmukh", "High", 0.89, "Financial aid referral", "2026-08-20", "2026-09-12", "Enrolled", 8.0, 0.30, "Improved", "Received emergency grant; tuition delinquency cleared.")
        ]

        for i_id, s_id, s_name, irisk, iprob, itype, idate, fdate, est, att_ch, gpa_ch, st, nts in sample_outcomes:
            cursor.execute("""
                INSERT INTO outcomes_tracking (
                    intervention_id, student_id, student_name, initial_risk_level, initial_risk_prob,
                    intervention_type, intervention_date, follow_up_date, enrollment_status,
                    attendance_change, gpa_change, academic_progress_status, outcome_notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (i_id, s_id, s_name, irisk, iprob, itype, idate, fdate, est, att_ch, gpa_ch, st, nts))

        conn.commit()

    conn.close()

def get_all_students(search=None, department=None, semester=None, risk_level=None, attendance_min=None, attendance_max=None):
    conn = get_connection()
    query = "SELECT * FROM students WHERE 1=1"
    params = []

    if search:
        query += " AND (student_id LIKE ? OR name LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    if department and department != "All Departments":
        query += " AND department = ?"
        params.append(department)
    if semester and semester != "All Semesters":
        query += " AND semester = ?"
        params.append(int(semester))
    if risk_level and risk_level != "All Risk Levels":
        query += " AND risk_level = ?"
        params.append(risk_level)
    if attendance_min is not None:
        query += " AND attendance_rate >= ?"
        params.append(float(attendance_min))
    if attendance_max is not None:
        query += " AND attendance_rate <= ?"
        params.append(float(attendance_max))

    query += " ORDER BY risk_probability DESC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_student_by_id(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def add_student(student):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO students (
            student_id, name, department, semester, attendance_rate, gpa,
            previous_gpa, gpa_change, assignment_completion_rate, late_submissions_count,
            library_visits_monthly, lms_login_frequency_weekly, financial_aid_status,
            tuition_fee_delinquent, failed_courses_count, dropout_target, risk_level,
            risk_probability, last_follow_up, counsellor_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student['student_id'], student['name'], student['department'], int(student['semester']),
        float(student['attendance_rate']), float(student['gpa']), float(student['previous_gpa']), float(student['gpa_change']),
        float(student['assignment_completion_rate']), int(student['late_submissions_count']),
        int(student['library_visits_monthly']), int(student['lms_login_frequency_weekly']),
        student['financial_aid_status'], int(student['tuition_fee_delinquent']), int(student['failed_courses_count']),
        int(student.get('dropout_target', 0)), student['risk_level'], float(student['risk_probability']),
        student.get('last_follow_up', 'None'), student.get('counsellor_notes', 'Record created.')
    ))
    conn.commit()
    conn.close()

def batch_add_students(df):
    for _, row in df.iterrows():
        add_student(row.to_dict())

def update_student_notes(student_id, notes, follow_up_date=None):
    conn = get_connection()
    cursor = conn.cursor()
    if follow_up_date:
        cursor.execute("UPDATE students SET counsellor_notes = ?, last_follow_up = ? WHERE student_id = ?", (notes, follow_up_date, student_id))
    else:
        cursor.execute("UPDATE students SET counsellor_notes = ? WHERE student_id = ?", (notes, student_id))
    conn.commit()
    conn.close()

def get_interventions(student_id=None, status=None, intervention_type=None):
    conn = get_connection()
    query = "SELECT * FROM interventions WHERE 1=1"
    params = []
    if student_id:
        query += " AND student_id = ?"
        params.append(student_id)
    if status and status != "All":
        query += " AND status = ?"
        params.append(status)
    if intervention_type and intervention_type != "All":
        query += " AND intervention_type = ?"
        params.append(intervention_type)
    query += " ORDER BY id DESC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def add_intervention(inv):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO interventions (
            student_id, student_name, intervention_type, assigned_counsellor,
            creation_date, follow_up_date, status, notes, outcome
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        inv['student_id'], inv['student_name'], inv['intervention_type'],
        inv['assigned_counsellor'], inv['creation_date'], inv['follow_up_date'],
        inv['status'], inv.get('notes', ''), inv.get('outcome', '')
    ))

    # Update student's last follow up date & notes
    cursor.execute("UPDATE students SET last_follow_up = ? WHERE student_id = ?", (inv['creation_date'], inv['student_id']))

    conn.commit()
    conn.close()

def update_intervention(inv_id, status=None, notes=None, outcome=None):
    conn = get_connection()
    cursor = conn.cursor()
    fields = []
    params = []
    if status:
        fields.append("status = ?")
        params.append(status)
    if notes is not None:
        fields.append("notes = ?")
        params.append(notes)
    if outcome is not None:
        fields.append("outcome = ?")
        params.append(outcome)

    if fields:
        params.append(inv_id)
        query = f"UPDATE interventions SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
    conn.close()

def get_outcomes():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM outcomes_tracking ORDER BY id DESC", conn)
    conn.close()
    return df

def add_outcome(out):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO outcomes_tracking (
            intervention_id, student_id, student_name, initial_risk_level, initial_risk_prob,
            intervention_type, intervention_date, follow_up_date, enrollment_status,
            attendance_change, gpa_change, academic_progress_status, outcome_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        out.get('intervention_id', 0), out['student_id'], out['student_name'],
        out['initial_risk_level'], float(out['initial_risk_prob']), out['intervention_type'],
        out['intervention_date'], out['follow_up_date'], out['enrollment_status'],
        float(out['attendance_change']), float(out['gpa_change']), out['academic_progress_status'],
        out.get('outcome_notes', '')
    ))
    conn.commit()
    conn.close()

def get_dashboard_metrics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM students WHERE risk_level = 'High'")
    high_risk = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM students WHERE risk_level IN ('High', 'Medium') AND (last_follow_up IS NULL OR last_follow_up = 'None')")
    needing_followup = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM outcomes_tracking WHERE enrollment_status = 'Enrolled'")
    successful_interventions = cursor.fetchone()[0]

    conn.close()
    return {
        "total_students": total_students,
        "high_risk": high_risk,
        "needing_followup": needing_followup,
        "successful_interventions": successful_interventions
    }
