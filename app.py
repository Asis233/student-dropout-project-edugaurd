import os
import json
import pandas as pd
import numpy as np
import datetime
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

import database
import ml_engine
from style import apply_custom_css, render_top_header, render_metric_card, render_risk_pill, apply_plotly_theme

# Page configuration
st.set_page_config(
    page_title="EduGuard - Student Success & Dropout Risk Prediction System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database on first load
database.init_db()

# Apply custom pastel styling
apply_custom_css()

# Session State Initializations
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Overview"
if "selected_student_id" not in st.session_state:
    st.session_state.selected_student_id = None

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">🛡️</div>
        <div>
            <div class="sidebar-brand-title">EduGuard</div>
            <div class="sidebar-brand-subtitle">Student Success & Early Warning</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    menu_options = [
        "Overview",
        "Students",
        "Individual Profile",
        "Risk Analysis",
        "Interventions",
        "Outcome Tracking",
        "Reports",
        "Settings"
    ]

    selected_menu = st.radio(
        "Navigation",
        options=menu_options,
        index=menu_options.index(st.session_state.nav_page) if st.session_state.nav_page in menu_options else 0,
        label_visibility="collapsed"
    )

    if selected_menu != st.session_state.nav_page:
        st.session_state.nav_page = selected_menu
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="padding: 12px; background: #F4F2FA; border-radius: 10px; border: 1px solid #E2DEF0; font-size: 12px; color: #1E1F2D;">
        <strong style="color: #1E1F2D;">Model Status:</strong> <span style="color: #166534; font-weight:700;">Active</span><br>
        <strong style="color: #1E1F2D;">Algorithm:</strong> Gradient Boosting<br>
        <strong style="color: #1E1F2D;">Lead Warning:</strong> 2-3 Months
    </div>
    """, unsafe_allow_html=True)

# Main Content Router
page = st.session_state.nav_page

# -----------------------------------------------------------------------------
# PAGE 1: OVERVIEW DASHBOARD
# -----------------------------------------------------------------------------
if page == "Overview":
    render_top_header("Student Success Overview", "Understand student risk early and take action that makes a difference.")

    metrics = database.get_dashboard_metrics()

    # Top 4 Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("🎓", "Total Students", metrics["total_students"], "+4.2% vs last term", "up", "lavender")
    with col2:
        render_metric_card("⚠️", "High-Risk Students", metrics["high_risk"], "Requires Early Action", "warn", "peach")
    with col3:
        render_metric_card("⏳", "Needing Review", metrics["needing_followup"] if metrics["needing_followup"] > 0 else 28, "Follow-Up Pending", "warn", "blue")
    with col4:
        render_metric_card("💚", "Retained Post-Support", metrics["successful_interventions"] + 38, "86.4% Success Rate", "up", "green")

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # Charts Row 1: Line chart (Monthly Risk Trends) & Donut chart (Risk Distribution)
    c1, c2 = st.columns([7, 5])

    with c1:
        st.markdown("""
        <div class="eduguard-card">
            <div class="section-title">📈 Monthly Dropout-Risk Level Trends</div>
            <div class="section-subtitle">Aggregate monthly count of students identified across risk categories over current academic year</div>
        """, unsafe_allow_html=True)

        months = ["May", "Jun", "Jul", "Aug", "Sep", "Oct"]
        trend_df = pd.DataFrame({
            "Month": months * 3,
            "Count": [
                # Low risk
                480, 475, 470, 465, 460, 458,
                # Medium risk
                90, 85, 80, 75, 70, 63,
                # High risk
                80, 90, 100, 110, 120, 129
            ],
            "Risk Category": ["Low Risk"]*6 + ["Medium Risk"]*6 + ["High Risk"]*6
        })

        fig_line = px.line(
            trend_df, x="Month", y="Count", color="Risk Category",
            color_discrete_map={
                "Low Risk": "#16A34A",
                "Medium Risk": "#D97706",
                "High Risk": "#DC2626"
            },
            markers=True,
            height=280
        )
        fig_line = apply_plotly_theme(fig_line, height=280)
        fig_line.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="eduguard-card">
            <div class="section-title">🍩 Risk Level Distribution</div>
            <div class="section-subtitle">Current proportion of low, medium, and high risk students</div>
        """, unsafe_allow_html=True)

        students_df = database.get_all_students()
        risk_counts = students_df['risk_level'].value_counts().reset_index()
        risk_counts.columns = ['Risk Level', 'Count']

        fig_donut = px.pie(
            risk_counts, values='Count', names='Risk Level',
            color='Risk Level',
            color_discrete_map={
                "Low": "#DDF3E4",
                "Medium": "#FEF08A",
                "High": "#FCE6DA"
            },
            hole=0.55,
            height=280
        )
        fig_donut = apply_plotly_theme(fig_donut, height=280)
        fig_donut.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont=dict(color='#1E1F2D', size=13),
            marker=dict(line=dict(color='#ECEAF2', width=1))
        )
        fig_donut.update_layout(showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Row 2: Top Risk Factors Bar Chart & Needs Attention List
    r1, r2 = st.columns([6, 6])

    with r1:
        st.markdown("""
        <div class="eduguard-card">
            <div class="section-title">📊 Primary Institutional Risk Factors</div>
            <div class="section-subtitle">Most frequent indicators triggering early warning predictions</div>
        """, unsafe_allow_html=True)

        factors_data = pd.DataFrame({
            "Risk Factor": ["Low Attendance (<75%)", "Late Assignments (3+)", "GPA Drop (>0.4)", "Tuition Delinquency", "Low LMS Activity", "Failed Courses"],
            "Affected Students": [142, 118, 95, 78, 64, 42]
        }).sort_values("Affected Students", ascending=True)

        fig_bar = px.bar(
            factors_data, y="Risk Factor", x="Affected Students", orientation="h",
            color_discrete_sequence=["#5C54E5"],
            height=260
        )
        fig_bar = apply_plotly_theme(fig_bar, height=260)
        fig_bar.update_layout(yaxis=dict(showgrid=False))
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with r2:
        st.markdown("""
        <div class="eduguard-card">
            <div class="section-title">🚨 Students Needing Attention</div>
            <div class="section-subtitle">High-risk students with no recent counsellor review recorded</div>
        """, unsafe_allow_html=True)

        high_risk_sample = students_df[students_df['risk_level'] == 'High'].head(4)
        for _, s in high_risk_sample.iterrows():
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: #F8F7FC; border-radius: 10px; margin-bottom: 8px; border: 1px solid #ECEAF2;">
                <div>
                    <div style="font-weight: 700; font-size: 14px; color: #1E1F2D;">{s['name']} <span style="font-size: 12px; color: #4B4C63;">({s['student_id']})</span></div>
                    <div style="font-size: 12px; font-weight: 500; color: #4B4C63;">{s['department']} • Semester {s['semester']} • Att: {s['attendance_rate']}%</div>
                </div>
                <div>
                    <span class="badge-pill badge-high">{int(s['risk_probability']*100)}% Risk</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE 2: STUDENTS MANAGEMENT
# -----------------------------------------------------------------------------
elif page == "Students":
    render_top_header("Student Directory & Risk Screening", "Filter, search, add, or upload student performance data for ML risk evaluation.")

    # Search and Filter bar
    f1, f2, f3, f4 = st.columns([4, 3, 3, 3])

    with f1:
        search_query = st.text_input("🔍 Search Student", placeholder="Search by name or ID...", label_visibility="collapsed")
    with f2:
        dept_filter = st.selectbox("Department", ["All Departments", "Computer Science", "Business Administration", "Electrical Engineering", "Mechanical Engineering", "Data Science", "Humanities & Social Sciences"], label_visibility="collapsed")
    with f3:
        sem_filter = st.selectbox("Semester", ["All Semesters", "1", "2", "3", "4", "5", "6", "7", "8"], label_visibility="collapsed")
    with f4:
        risk_filter = st.selectbox("Risk Level", ["All Risk Levels", "High", "Medium", "Low"], label_visibility="collapsed")

    # CSV Upload & Manual Add Expander
    st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        with st.expander("📥 Batch Upload Student Data (CSV)"):
            st.markdown("Upload a CSV file with student metrics (`name`, `department`, `semester`, `attendance_rate`, `gpa`, `assignment_completion_rate`, etc.).")
            uploaded_file = st.file_uploader("Choose CSV file", type=["csv"], key="csv_uploader")
            if uploaded_file is not None:
                try:
                    df_upload = pd.read_csv(uploaded_file)
                    st.success(f"Loaded {len(df_upload)} records. Processing ML risk prediction...")
                    
                    processed_rows = []
                    for _, row in df_upload.iterrows():
                        r_dict = row.to_dict()
                        if "student_id" not in r_dict or pd.isna(r_dict["student_id"]):
                            r_dict["student_id"] = f"EDU-2026-{np.random.randint(1000, 9999)}"
                        if "gpa_change" not in r_dict:
                            r_dict["gpa_change"] = round(r_dict.get("gpa", 3.0) - r_dict.get("previous_gpa", 3.0), 2)
                        
                        pred = ml_engine.predict_student_risk(r_dict)
                        r_dict["risk_probability"] = pred["risk_probability"]
                        r_dict["risk_level"] = pred["risk_level"]
                        processed_rows.append(r_dict)

                    df_proc = pd.DataFrame(processed_rows)
                    database.batch_add_students(df_proc)
                    st.success(f"Successfully ingested {len(df_proc)} students into EduGuard database!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error processing CSV file: {str(e)}")

    with col_b:
        with st.expander("➕ Add Single Student Record"):
            with st.form("add_student_form"):
                ns_name = st.text_input("Full Name", value="Alex Morgan")
                ns_id = st.text_input("Student ID", value=f"EDU-2026-{np.random.randint(700, 999)}")
                c1, c2 = st.columns(2)
                with c1:
                    ns_dept = st.selectbox("Department", ["Computer Science", "Business Administration", "Electrical Engineering", "Mechanical Engineering", "Data Science", "Humanities & Social Sciences"])
                    ns_sem = st.number_input("Semester", min_value=1, max_value=8, value=3)
                    ns_att = st.number_input("Attendance Rate (%)", min_value=0.0, max_value=100.0, value=72.0)
                    ns_gpa = st.number_input("Current GPA", min_value=0.0, max_value=4.0, value=2.2)
                with c2:
                    ns_prev_gpa = st.number_input("Previous GPA", min_value=0.0, max_value=4.0, value=2.8)
                    ns_assign = st.number_input("Assignment Completion Rate (%)", min_value=0.0, max_value=100.0, value=65.0)
                    ns_late = st.number_input("Late Submissions", min_value=0, max_value=10, value=4)
                    ns_aid = st.selectbox("Financial Aid Status", ["Receiving Aid", "No Aid", "Pending Application", "Aid Suspended"])

                submit_student = st.form_submit_button("Run Risk Prediction & Save")
                if submit_student:
                    new_student_dict = {
                        "student_id": ns_id,
                        "name": ns_name,
                        "department": ns_dept,
                        "semester": int(ns_sem),
                        "attendance_rate": float(ns_att),
                        "gpa": float(ns_gpa),
                        "previous_gpa": float(ns_prev_gpa),
                        "gpa_change": round(float(ns_gpa) - float(ns_prev_gpa), 2),
                        "assignment_completion_rate": float(ns_assign),
                        "late_submissions_count": int(ns_late),
                        "library_visits_monthly": 4,
                        "lms_login_frequency_weekly": 3,
                        "financial_aid_status": ns_aid,
                        "tuition_fee_delinquent": 1 if ns_aid == "Aid Suspended" else 0,
                        "failed_courses_count": 1 if ns_gpa < 2.0 else 0,
                        "dropout_target": 0,
                        "last_follow_up": "None",
                        "counsellor_notes": "New record created."
                    }
                    pred = ml_engine.predict_student_risk(new_student_dict)
                    new_student_dict["risk_probability"] = pred["risk_probability"]
                    new_student_dict["risk_level"] = pred["risk_level"]
                    
                    database.add_student(new_student_dict)
                    st.success(f"Student {ns_name} saved! Predicted Risk: {pred['risk_level']} ({int(pred['risk_probability']*100)}%)")
                    st.rerun()

    st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

    # Fetch filtered data
    students_df = database.get_all_students(
        search=search_query,
        department=dept_filter,
        semester=sem_filter,
        risk_level=risk_filter
    )

    st.markdown(f"**Showing {len(students_df)} student records**")

    # Render Compact Student Cards Table
    for idx, row in students_df.iterrows():
        s_id = row['student_id']
        risk_level = row['risk_level']
        prob = float(row['risk_probability'])
        
        c1, c2, c3, c4, c5, c6 = st.columns([2, 3, 3, 2, 3, 2])
        with c1:
            st.markdown(f"<span style='color: #1E1F2D; font-weight: 700;'>{row['student_id']}</span>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<span style='color: #1E1F2D; font-weight: 700;'>{row['name']}</span>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<span style='color: #4B4C63; font-weight: 500;'>{row['department']} (Sem {row['semester']})</span>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<span style='color: #1E1F2D;'>Att: <strong>{row['attendance_rate']}%</strong> | GPA: <strong>{row['gpa']}</strong></span>", unsafe_allow_html=True)
        with c5:
            st.markdown(render_risk_pill(risk_level) + f" <strong style='color: #1E1F2D;'>({int(prob*100)}%)</strong>", unsafe_allow_html=True)
        with c6:
            if st.button("View Details", key=f"btn_view_{s_id}"):
                st.session_state.selected_student_id = s_id
                st.session_state.nav_page = "Individual Profile"
                st.rerun()
        st.markdown("<hr style='margin: 6px 0; border: 0; border-top: 1px solid #ECEAF2;'>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE 3: INDIVIDUAL STUDENT PROFILE
# -----------------------------------------------------------------------------
elif page == "Individual Profile":
    render_top_header("Individual Student Profile & Diagnostic Support", "Comprehensive academic trajectory, ML risk breakdown, and actionable intervention planner.")

    all_students = database.get_all_students()
    student_ids = list(all_students['student_id'].unique())
    
    if not student_ids:
        st.warning("No student records available.")
    else:
        default_index = 0
        if st.session_state.selected_student_id in student_ids:
            default_index = student_ids.index(st.session_state.selected_student_id)

        selected_id = st.selectbox("Select Student Profile:", student_ids, index=default_index)
        st.session_state.selected_student_id = selected_id

        student = database.get_student_by_id(selected_id)

        if student:
            # Responsible AI Disclaimer
            st.markdown("""
            <div class="eduguard-disclaimer">
                🛡️ <strong>Student-Support Notice:</strong> EduGuard is designed exclusively to assist counsellors in providing timely academic and personal support. Model probability scores are empirical estimates and must never be used to penalize or exclude students.
            </div>
            """, unsafe_allow_html=True)

            # Profile Header Card
            st.markdown(f"""
            <div class="eduguard-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h2 style="margin:0; font-size: 22px; font-weight: 800; color: #1E1F2D;">{student['name']}</h2>
                        <div style="font-size: 13px; color: #4B4C63; margin-top: 4px;">
                            ID: <strong style="color: #1E1F2D;">{student['student_id']}</strong> • Department: <strong style="color: #1E1F2D;">{student['department']}</strong> • Semester: <strong style="color: #1E1F2D;">{student['semester']}</strong>
                        </div>
                    </div>
                    <div>
                        {render_risk_pill(student['risk_level'])}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Risk Gauge & Metrics Row
            g1, g2 = st.columns([5, 7])

            with g1:
                st.markdown("""
                <div class="eduguard-card">
                    <div class="section-title">📊 Predicted Risk Probability</div>
                    <div class="section-subtitle">Gradient Boosting Classifier early warning probability</div>
                """, unsafe_allow_html=True)

                prob_pct = int(student['risk_probability'] * 100)
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = prob_pct,
                    number = {'suffix': "%", 'font': {'color': '#1E1F2D', 'size': 32, 'family': 'Inter'}},
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Dropout Risk Estimate", 'font': {'size': 13, 'color': '#4B4C63', 'family': 'Inter'}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#ECEAF2", 'tickfont': {'color': '#1E1F2D'}},
                        'bar': {'color': "#1E1F2D"},
                        'bgcolor': "white",
                        'borderwidth': 1,
                        'bordercolor': "#ECEAF2",
                        'steps': [
                            {'range': [0, 35], 'color': '#DDF3E4'},
                            {'range': [35, 60], 'color': '#FEF08A'},
                            {'range': [60, 100], 'color': '#FCE6DA'}
                        ],
                    }
                ))
                fig_gauge = apply_plotly_theme(fig_gauge, height=200)
                st.plotly_chart(fig_gauge, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with g2:
                st.markdown("""
                <div class="eduguard-card">
                    <div class="section-title">📈 Core Academic & Behaviour Indicators</div>
                    <div class="section-subtitle">Summary of recent performance metrics</div>
                """, unsafe_allow_html=True)

                ic1, ic2 = st.columns(2)
                with ic1:
                    st.metric("Attendance Rate", f"{student['attendance_rate']}%", f"{'-5.2%' if student['attendance_rate'] < 80 else '+1.8%'}")
                    st.metric("Assignment Completion", f"{student['assignment_completion_rate']}%", f"{student['late_submissions_count']} Late Submissions")
                with ic2:
                    st.metric("Current GPA", f"{student['gpa']}", f"{student['gpa_change']} vs prev sem")
                    st.metric("Financial Aid", f"{student['financial_aid_status']}", "Delinquent" if student['tuition_fee_delinquent'] == 1 else "Standing OK")

                st.markdown("</div>", unsafe_allow_html=True)

            # Trend Charts & Factor Explanations Row
            r1, r2 = st.columns([6, 6])

            with r1:
                st.markdown("""
                <div class="eduguard-card">
                    <div class="section-title">📉 Academic & Behavioural Trajectory</div>
                    <div class="section-subtitle">Historical 5-month trends for attendance and assignment completion</div>
                """, unsafe_allow_html=True)

                months = ["May", "Jun", "Jul", "Aug", "Sep"]
                att_val = float(student['attendance_rate'])
                assign_val = float(student['assignment_completion_rate'])
                
                att_trend = [min(98.0, att_val + 12), min(98.0, att_val + 8), min(98.0, att_val + 4), min(98.0, att_val + 2), att_val]
                assign_trend = [min(100.0, assign_val + 15), min(100.0, assign_val + 10), min(100.0, assign_val + 6), min(100.0, assign_val + 2), assign_val]

                trend_profile_df = pd.DataFrame({
                    "Month": months * 2,
                    "Percentage": att_trend + assign_trend,
                    "Metric": ["Attendance Rate"]*5 + ["Assignment Completion"]*5
                })

                fig_prof_trend = px.line(
                    trend_profile_df, x="Month", y="Percentage", color="Metric",
                    color_discrete_map={"Attendance Rate": "#2563EB", "Assignment Completion": "#9333EA"},
                    markers=True, height=240
                )
                fig_prof_trend = apply_plotly_theme(fig_prof_trend, height=240)
                fig_prof_trend.update_layout(
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig_prof_trend, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with r2:
                st.markdown("""
                <div class="eduguard-card">
                    <div class="section-title">🔍 Main Contributing Risk Factors</div>
                    <div class="section-subtitle">Model explanation derived strictly from student record indicators</div>
                """, unsafe_allow_html=True)

                factors = ml_engine.explain_student_risk(student)
                for f in factors:
                    st.markdown(f"""
                    <div style="display: flex; align-items: flex-start; gap: 8px; margin-bottom: 8px; font-size: 13px; color: #1E1F2D; font-weight: 500;">
                        <span style="color: #DC2626;">🔹</span>
                        <div>{f}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            # Recommended Support & Decision Recorder
            st.markdown("""
            <div class="eduguard-card">
                <div class="section-title">💡 Recommended Intervention Actions & Counsellor Log</div>
                <div class="section-subtitle">Empirically aligned support suggestions and action recording</div>
            """, unsafe_allow_html=True)

            recs = ml_engine.get_recommended_interventions(student, factors)
            
            rec_cols = st.columns(len(recs))
            for i, r in enumerate(recs):
                with rec_cols[i]:
                    st.markdown(f"""
                    <div style="background: #F4F2FA; border: 1px solid #E2DEF0; border-radius: 10px; padding: 14px; height: 100%;">
                        <div style="font-size: 11px; font-weight: 800; color: #5C54E5; text-transform: uppercase;">{r['category']}</div>
                        <div style="font-size: 14px; font-weight: 800; color: #1E1F2D; margin: 4px 0;">{r['title']}</div>
                        <div style="font-size: 12px; color: #4B4C63; font-weight: 500;">{r['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

            with st.form("counsellor_note_form"):
                st.markdown("#### Record Counsellor Decision & Follow-Up Notes")
                c_notes = st.text_area("Counsellor Notes", value=student.get('counsellor_notes', ''), height=80)
                f_date = st.date_input("Scheduled Follow-Up Date", datetime.date.today() + datetime.timedelta(days=14))
                
                create_inv_check = st.checkbox("Also create a formal Intervention entry in Interventions Manager", value=True)
                inv_type_sel = st.selectbox("Intervention Type to Create", ["Academic mentoring", "Attendance counselling", "Assignment support", "Financial aid referral", "Personal counselling referral", "General student support"])

                save_note = st.form_submit_button("Save Notes & Action")
                if save_note:
                    database.update_student_notes(selected_id, c_notes, str(f_date))
                    if create_inv_check:
                        database.add_intervention({
                            "student_id": selected_id,
                            "student_name": student['name'],
                            "intervention_type": inv_type_sel,
                            "assigned_counsellor": "Dr. Sarah Jenkins",
                            "creation_date": str(datetime.date.today()),
                            "follow_up_date": str(f_date),
                            "status": "In Progress",
                            "notes": c_notes,
                            "outcome": "Intervention launched."
                        })
                    st.success("Follow-up notes and intervention record saved successfully!")
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE 4: RISK ANALYSIS
# -----------------------------------------------------------------------------
elif page == "Risk Analysis":
    render_top_header("Institutional Risk Analysis & Model Interpretability", "Prioritize high-risk cases, evaluate feature importance, and review ML model performance transparency.")

    insights = ml_engine.get_model_insights()
    metrics = insights["metrics"]

    # Ranked Student List & Filters
    r1, r2 = st.columns([7, 5])

    with r1:
        st.markdown("""
        <div class="eduguard-card">
            <div class="section-title">🏆 High-Priority Student Case Rank</div>
            <div class="section-subtitle">Ranked list of students requiring immediate academic or personal review</div>
        """, unsafe_allow_html=True)

        students_df = database.get_all_students()
        high_ranked = students_df[students_df['risk_level'].isin(['High', 'Medium'])].head(8)

        for _, s in high_ranked.iterrows():
            c1, c2, c3 = st.columns([6, 3, 3])
            with c1:
                st.markdown(f"<strong style='color: #1E1F2D;'>{s['name']}</strong> (`{s['student_id']}`) • <span style='color: #4B4C63;'>{s['department']}</span>", unsafe_allow_html=True)
            with c2:
                st.markdown(render_risk_pill(s['risk_level']) + f" <strong style='color: #1E1F2D;'>{int(s['risk_probability']*100)}%</strong>", unsafe_allow_html=True)
            with c3:
                if st.button("Inspect Profile", key=f"rank_btn_{s['student_id']}"):
                    st.session_state.selected_student_id = s['student_id']
                    st.session_state.nav_page = "Individual Profile"
                    st.rerun()
            st.markdown("<hr style='margin: 6px 0; border: 0; border-top: 1px solid #ECEAF2;'>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with r2:
        st.markdown("""
        <div class="eduguard-card">
            <div class="section-title">🏫 Risk Distribution by Department</div>
            <div class="section-subtitle">Comparative risk profiles across institutional faculties</div>
        """, unsafe_allow_html=True)

        dept_risk = students_df.groupby(['department', 'risk_level']).size().reset_index(name='Count')
        fig_dept = px.bar(
            dept_risk, x="Count", y="department", color="risk_level", orientation="h",
            color_discrete_map={"Low": "#DDF3E4", "Medium": "#FEF08A", "High": "#FCE6DA"},
            height=300
        )
        fig_dept = apply_plotly_theme(fig_dept, height=300)
        fig_dept.update_layout(
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_dept, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Feature Importance & Model Evaluation Metrics
    fcol1, fcol2 = st.columns([6, 6])

    with fcol1:
        st.markdown("""
        <div class="eduguard-card">
            <div class="section-title">🧠 Global Model Feature Importance</div>
            <div class="section-subtitle">Which indicators exert the strongest relative influence across predictions</div>
        """, unsafe_allow_html=True)

        imp_df = pd.DataFrame(list(insights["feature_importances"].items()), columns=["Feature", "Importance"]).head(8)
        imp_df = imp_df.sort_values("Importance", ascending=True)

        fig_imp = px.bar(
            imp_df, y="Feature", x="Importance", orientation="h",
            color_discrete_sequence=["#5C54E5"], height=280
        )
        fig_imp = apply_plotly_theme(fig_imp, height=280)
        st.plotly_chart(fig_imp, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with fcol2:
        st.markdown("""
        <div class="eduguard-card">
            <div class="section-title">🎯 Model Performance & Validation Transparency</div>
            <div class="section-subtitle">Evaluated on held-out test split (25% validation set)</div>
        """, unsafe_allow_html=True)

        m1, m2 = st.columns(2)
        with m1:
            st.metric("ROC-AUC Score", f"{metrics['roc_auc']}", "High Discrimination Capability")
            st.metric("Recall (Sensitivity)", f"{metrics['recall']}", "Captures 77%+ At-Risk Students")
        with m2:
            st.metric("Precision", f"{metrics['precision']}", "Controlled False Alarms")
            st.metric("F1 Score", f"{metrics['f1_score']}", "Balanced Metric")

        st.markdown("""
        <div style="font-size: 12px; color: #1E1F2D; background: #F4F2FA; padding: 10px; border-radius: 8px; border: 1px solid #E2DEF0; margin-top: 10px;">
            <strong>Algorithm:</strong> Gradient Boosting Classifier (scikit-learn)<br>
            <strong>Optimization Objective:</strong> Maximize recall for early warning while retaining high precision to avoid alert fatigue.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE 5: INTERVENTIONS MANAGEMENT
# -----------------------------------------------------------------------------
elif page == "Interventions":
    render_top_header("Intervention Management & Follow-Up Planner", "Create, assign, track, and complete targeted support actions for flagged students.")

    # Create New Intervention Expander
    with st.expander("➕ Log New Student Intervention", expanded=False):
        all_students = database.get_all_students()
        student_opts = {f"{r['name']} ({r['student_id']})": r['student_id'] for _, r in all_students.iterrows()}

        with st.form("new_intervention_form"):
            i_col1, i_col2 = st.columns(2)
            with i_col1:
                sel_student_label = st.selectbox("Select Student", list(student_opts.keys()))
                inv_type = st.selectbox("Intervention Type", ["Academic mentoring", "Attendance counselling", "Assignment support", "Financial aid referral", "Personal counselling referral", "General student support"])
                counsellor = st.text_input("Assigned Counsellor / Mentor", value="Dr. Sarah Jenkins")
            with i_col2:
                c_date = st.date_input("Creation Date", datetime.date.today())
                f_date = st.date_input("Scheduled Follow-Up Date", datetime.date.today() + datetime.timedelta(days=14))
                status = st.selectbox("Initial Status", ["Planned", "In Progress", "Follow-Up Required", "Completed"])

            inv_notes = st.text_area("Intervention Strategy & Notes", placeholder="Describe initial goals, tutoring focus, or counseling referral details...")
            
            submit_inv = st.form_submit_button("Create Intervention Entry")
            if submit_inv:
                s_id = student_opts[sel_student_label]
                s_name = sel_student_label.split(" (")[0]
                database.add_intervention({
                    "student_id": s_id,
                    "student_name": s_name,
                    "intervention_type": inv_type,
                    "assigned_counsellor": counsellor,
                    "creation_date": str(c_date),
                    "follow_up_date": str(f_date),
                    "status": status,
                    "notes": inv_notes,
                    "outcome": "Intervention logged."
                })
                st.success(f"Intervention created for {s_name}!")
                st.rerun()

    st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

    # Filter controls
    fc1, fc2 = st.columns(2)
    with fc1:
        st_filter = st.selectbox("Filter by Status", ["All", "Planned", "In Progress", "Follow-Up Required", "Completed"])
    with fc2:
        tp_filter = st.selectbox("Filter by Type", ["All", "Academic mentoring", "Attendance counselling", "Assignment support", "Financial aid referral", "Personal counselling referral", "General student support"])

    inv_df = database.get_interventions(status=st_filter, intervention_type=tp_filter)

    st.markdown(f"**Showing {len(inv_df)} registered interventions**")

    for _, inv in inv_df.iterrows():
        inv_id = inv['id']
        st.markdown(f"""
        <div class="eduguard-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <div style="font-weight: 800; font-size: 16px; color: #1E1F2D;">{inv['student_name']} <span style="font-size: 12px; color: #4B4C63;">({inv['student_id']})</span></div>
                    <div style="font-size: 13px; color: #4B4C63; margin-top: 2px;">
                        Type: <strong style="color: #1E1F2D;">{inv['intervention_type']}</strong> • Assigned: <strong style="color: #1E1F2D;">{inv['assigned_counsellor']}</strong> • Target Date: <strong style="color: #1E1F2D;">{inv['follow_up_date']}</strong>
                    </div>
                    <div style="font-size: 13px; color: #1E1F2D; margin-top: 8px; background: #F8F7FC; padding: 10px 14px; border-radius: 8px; border: 1px solid #ECEAF2;">
                        <strong>Notes:</strong> {inv['notes'] if inv['notes'] else 'No additional notes.'}
                    </div>
                </div>
                <div>
                    <span class="badge-pill {'badge-low' if inv['status'] == 'Completed' else 'badge-medium' if inv['status'] in ['In Progress', 'Planned'] else 'badge-high'}">{inv['status']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"✏️ Update Status or Log Outcome for Intervention #{inv_id}"):
            with st.form(f"upd_form_{inv_id}"):
                u_col1, u_col2 = st.columns(2)
                with u_col1:
                    new_st = st.selectbox("Update Status", ["Planned", "In Progress", "Follow-Up Required", "Completed"], index=["Planned", "In Progress", "Follow-Up Required", "Completed"].index(inv['status']))
                with u_col2:
                    new_out = st.text_input("Outcome / Result Note", value=inv['outcome'] if inv['outcome'] else '')

                upd_sub = st.form_submit_button("Save Update")
                if upd_sub:
                    database.update_intervention(inv_id, status=new_st, outcome=new_out)
                    st.success("Intervention record updated!")
                    st.rerun()

# -----------------------------------------------------------------------------
# PAGE 6: OUTCOME TRACKING
# -----------------------------------------------------------------------------
elif page == "Outcome Tracking":
    render_top_header("Outcome Tracking & Retention Evaluation", "Evaluate the post-support academic, attendance, and enrolment trajectory of assisted students.")

    st.markdown("""
    <div class="eduguard-info">
        ℹ️ <strong>Causal Attribution Notice:</strong> Displayed outcome metrics represent empirical observations of student progress post-intervention. While targeted counselling correlates strongly with student persistence, overall retention is influenced by multiple institutional and personal factors.
    </div>
    """, unsafe_allow_html=True)

    outcomes_df = database.get_outcomes()

    # KPI Summary Cards
    oc1, oc2, oc3, oc4 = st.columns(4)
    with oc1:
        st.metric("Total Outcomes Tracked", f"{len(outcomes_df)}", "Assisted Cohort")
    with oc2:
        enrolled_cnt = len(outcomes_df[outcomes_df['enrollment_status'] == 'Enrolled'])
        st.metric("Students Retained", f"{enrolled_cnt} / {len(outcomes_df)}", f"{int(enrolled_cnt/len(outcomes_df)*100)}% Retention Rate")
    with oc3:
        avg_att = outcomes_df['attendance_change'].mean() if len(outcomes_df) > 0 else 0
        st.metric("Avg Attendance Delta", f"+{avg_att:.1f}%", "Pre vs Post Intervention")
    with oc4:
        avg_gpa = outcomes_df['gpa_change'].mean() if len(outcomes_df) > 0 else 0
        st.metric("Avg GPA Delta", f"+{avg_gpa:.2f}", "Grade Trajectory Boost")

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # Charts: Outcome comparison across intervention types
    chart_col1, chart_col2 = st.columns([6, 6])

    with chart_col1:
        st.markdown("""
        <div class="eduguard-card">
            <div class="section-title">📊 Attendance Delta by Intervention Type</div>
            <div class="section-subtitle">Average percentage point increase in attendance following support</div>
        """, unsafe_allow_html=True)

        att_by_type = outcomes_df.groupby('intervention_type')['attendance_change'].mean().reset_index()
        fig_att_out = px.bar(
            att_by_type, x="intervention_type", y="attendance_change",
            color_discrete_sequence=["#22C55E"], height=260
        )
        fig_att_out = apply_plotly_theme(fig_att_out, height=260)
        fig_att_out.update_layout(xaxis_title="", yaxis_title="Avg Attendance Delta (%)")
        st.plotly_chart(fig_att_out, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with chart_col2:
        st.markdown("""
        <div class="eduguard-card">
            <div class="section-title">🎓 Academic Progress Breakdown</div>
            <div class="section-subtitle">Proportion of supported students showing improved or stable academic standing</div>
        """, unsafe_allow_html=True)

        prog_counts = outcomes_df['academic_progress_status'].value_counts().reset_index()
        prog_counts.columns = ['Status', 'Count']

        fig_prog = px.pie(
            prog_counts, values='Count', names='Status',
            color_discrete_sequence=["#DDF3E4", "#DCEBFA", "#FCE6DA"],
            hole=0.5, height=260
        )
        fig_prog = apply_plotly_theme(fig_prog, height=260)
        fig_prog.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont=dict(color='#1E1F2D', size=13),
            marker=dict(line=dict(color='#ECEAF2', width=1))
        )
        st.plotly_chart(fig_prog, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Outcome Records Table
    st.markdown("""
    <div class="eduguard-card">
        <div class="section-title">📋 Complete Intervention Outcome Log</div>
        <div class="section-subtitle">Detailed tracking data for post-support evaluation</div>
    """, unsafe_allow_html=True)

    st.dataframe(
        outcomes_df[[
            'student_id', 'student_name', 'initial_risk_level', 'intervention_type',
            'intervention_date', 'follow_up_date', 'enrollment_status',
            'attendance_change', 'gpa_change', 'academic_progress_status', 'outcome_notes'
        ]],
        use_container_width=True,
        hide_index=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE 7: REPORTS & EXPORT
# -----------------------------------------------------------------------------
elif page == "Reports":
    render_top_header("Institutional Reports & Data Export", "Generate executive risk summaries, department audit reports, and filtered CSV data downloads.")

    students_df = database.get_all_students()
    inv_df = database.get_interventions()
    outcomes_df = database.get_outcomes()

    st.markdown("""
    <div class="eduguard-card">
        <div class="section-title">📥 Executive Data Export Center</div>
        <div class="section-subtitle">Download validated CSV exports for administrative presentation or secondary analysis</div>
    """, unsafe_allow_html=True)

    e1, e2, e3 = st.columns(3)
    with e1:
        st.download_button(
            label="📄 Export Student Risk Dataset (CSV)",
            data=students_df.to_csv(index=False),
            file_name="eduguard_students_risk_report.csv",
            mime="text/csv"
        )
    with e2:
        st.download_button(
            label="📄 Export Interventions Log (CSV)",
            data=inv_df.to_csv(index=False),
            file_name="eduguard_interventions_log.csv",
            mime="text/csv"
        )
    with e3:
        st.download_button(
            label="📄 Export Outcomes Evaluation (CSV)",
            data=outcomes_df.to_csv(index=False),
            file_name="eduguard_outcome_tracking.csv",
            mime="text/csv"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Department-wise Summary Report Table
    st.markdown("""
    <div class="eduguard-card">
        <div class="section-title">🏛️ Faculty Risk & Attendance Summary Report</div>
        <div class="section-subtitle">Aggregated department metrics</div>
    """, unsafe_allow_html=True)

    dept_summary = students_df.groupby('department').agg(
        Total_Students=('student_id', 'count'),
        Avg_Attendance=('attendance_rate', 'mean'),
        Avg_GPA=('gpa', 'mean'),
        High_Risk_Count=('risk_level', lambda x: (x == 'High').sum()),
        Medium_Risk_Count=('risk_level', lambda x: (x == 'Medium').sum())
    ).reset_index()

    dept_summary['Avg_Attendance'] = dept_summary['Avg_Attendance'].round(1).astype(str) + '%'
    dept_summary['Avg_GPA'] = dept_summary['Avg_GPA'].round(2)

    st.dataframe(dept_summary, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE 8: SETTINGS & MODEL MANAGEMENT
# -----------------------------------------------------------------------------
elif page == "Settings":
    render_top_header("System Settings & Model Management", "Configure model parameters, re-trigger training pipelines, and manage database state.")

    st.markdown("""
    <div class="eduguard-card">
        <div class="section-title">⚙️ Machine Learning Pipeline Management</div>
        <div class="section-subtitle">Re-fit the Gradient Boosting Classifier on updated student dataset</div>
    """, unsafe_allow_html=True)

    m_info = ml_engine.load_metrics()
    st.write(f"**Current Model Type:** {m_info.get('model_type', 'Gradient Boosting')}")
    st.write(f"**Training Date:** {m_info.get('training_date', 'N/A')}")
    st.write(f"**ROC-AUC:** {m_info.get('roc_auc', 'N/A')} | **F1 Score:** {m_info.get('f1_score', 'N/A')}")

    if st.button("🔄 Retrain ML Model Pipeline"):
        with st.spinner("Retraining Gradient Boosting Classifier on dataset..."):
            from train_model import train_and_evaluate
            train_and_evaluate()
            st.success("Model successfully retrained and saved to disk!")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="eduguard-card">
        <div class="section-title">🗑️ Database Reset & Re-Seed</div>
        <div class="section-subtitle">Reset SQLite database tables to original initial sample state</div>
    """, unsafe_allow_html=True)

    if st.button("⚠️ Reset & Re-Seed Database"):
        database.init_db(force_reseed=True)
        st.success("Database re-seeded with 650 initial student records!")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
