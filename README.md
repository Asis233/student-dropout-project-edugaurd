# 🎓 EduGuard — Student Success & Dropout Risk Prediction System

> **Early Warning & Predictive Analytics Platform for Educational Institutions**  
> *Identify student risk 2–3 months in advance and deliver timely, compassionate academic & personal support.*

---

## 🌟 Project Overview

**EduGuard** is an end-to-end, AI/ML-powered predictive analytics SaaS platform designed for college counsellors, department heads, and academic advisors. By analyzing multi-dimensional student indicators—including academic trajectory, attendance trends, assignment submission behavior, library resource utilization, and financial aid status—EduGuard generates empirical dropout risk predictions with a lead time of 2–3 months.

### 🛡️ Responsible AI & Student-Support Framing
- **Empowerment over Exclusion:** EduGuard is built strictly as a student-support tool. It **never** automatically penalizes, excludes, or labels students.
- **Human-in-the-Loop:** All risk scores are presented as empirical model estimates to guide human counselling decisions.

---

## 🎨 Design & Theme

EduGuard features a modern, soft pastel SaaS design built to evoke clarity, calm, and professionalism:

- **Background:** `#F8F7FC`
- **Lavender Highlight:** `#DCD6F7`
- **Soft Blue:** `#DCEBFA`
- **Mint Green:** `#DDF3E4` (Low Risk Status / Positive Outcomes)
- **Pale Peach / Pink:** `#FCE6DA` / `#F8DFE8` (High Risk Warning)
- **Soft Amber:** `#FFF4D2` (Medium Risk Status)
- **Primary Text:** `#34354A`
- **Secondary Text:** `#77798B`
- **Borders & Cards:** `#ECEAF2` with 12px rounded corners and subtle shadows.

---

## 🧠 Machine Learning Architecture

- **Classifier:** `GradientBoostingClassifier` (scikit-learn).
- **Preprocessing:** `ColumnTransformer` with `StandardScaler` for numerical metrics and `OneHotEncoder` for categorical factors (department, financial aid status).
- **Validation Metrics:**
  - **ROC-AUC Score:** `0.887`
  - **Precision:** `67.3%`
  - **Recall (Sensitivity):** `77.1%` (Prioritizes early identification while keeping false alarms low).
  - **F1-Score:** `0.718`
- **Explainability:** Empirical feature importance attribution & individual student risk decomposition (explaining *why* a student was flagged without inventing causes).

---

## 📱 Application Pages

1. **Dashboard Overview (`Overview`):**
   - 4 metric cards (Total Students, High-Risk Students, Students Needing Follow-Up, Retained Post-Support).
   - Monthly risk trend line chart & risk level distribution donut chart.
   - Institutional primary risk factors bar chart.
   - "Needs Attention" table & Recent Activity feed.

2. **Student Directory & Risk Screening (`Students`):**
   - Search by name or ID.
   - Multi-attribute filters (Department, Semester, Risk Category).
   - Batch CSV upload with instant ML risk scoring.
   - Manual student entry form.
   - Compact table with pastel status pills and ML probability indicators.

3. **Individual Student Profile (`Individual Profile`):**
   - Comprehensive student summary card.
   - Risk probability gauge with explicit responsible AI disclaimer.
   - 5-month historical trend line charts (Attendance, GPA, Assignment completion).
   - Main empirical contributing factors.
   - Actionable recommended support actions.
   - Interactive Counsellor Notes & Decision Recorder.

4. **Risk Analysis (`Risk Analysis`):**
   - Ranked list of highest-priority cases.
   - Cross-faculty department risk comparison chart.
   - Global feature importance analysis.
   - Full model validation metrics & confusion matrix panel.

5. **Intervention Management (`Interventions`):**
   - Create, assign, and schedule targeted interventions (Academic mentoring, Attendance counselling, Assignment support, Financial aid referral, Personal counselling, General support).
   - Filterable interventions list with status updates (Planned, In Progress, Follow-Up Required, Completed).

6. **Outcome Tracking (`Outcome Tracking`):**
   - Tracks student retention post-support.
   - Attendance & GPA pre/post-intervention delta metrics.
   - Outcome breakdown charts across support types.
   - Causal attribution disclaimers.

7. **Reports & Data Export (`Reports`):**
   - Filtered CSV dataset exports (Students, Interventions, Outcomes).
   - Faculty risk summary report table.

8. **System Settings (`Settings`):**
   - One-click model retraining trigger.
   - Database reset & seed controls.

---

## 🚀 Quickstart & Installation

### Prerequisites
- Python 3.9+ (Python 3.10 – 3.14 supported)
- pip

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/your-repo/eduguard.git
cd eduguard
pip install -r requirements.txt
```

### 2. Generate Synthetic Dataset & Train Model
```bash
python generate_data.py
python train_model.py
```

### 3. Initialize Database & Launch Streamlit Web App
```bash
python -c "import database; database.init_db()"
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 📂 Project Structure

```
student dropout project/
├── data/
│   └── student_data.csv        # Synthetic student dataset (650 records)
├── models/
│   ├── eduguard_model.joblib   # Trained Gradient Boosting model pipeline
│   └── model_metrics.json      # Saved validation metrics & feature importances
├── app.py                      # Main Streamlit web application & page router
├── database.py                 # SQLite database helper module
├── generate_data.py            # Synthetic dataset generator
├── train_model.py              # ML training & evaluation pipeline
├── ml_engine.py                # Prediction inference, factor explanation & recommendations
├── style.py                    # Custom soft pastel CSS theme & UI helpers
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation & setup guide
```

---

## 🎤 Presentation Pitch Notes for College Judges

1. **Problem Statement:** College dropouts often happen silently when students struggle academically, financially, or personally. Traditional reviews occur too late (end of semester).
2. **The EduGuard Solution:** EduGuard acts as an **Early Warning System**, flagging risk 2–3 months before final assessments using a trained **Gradient Boosting classifier**.
3. **Data-Driven Interventions:** EduGuard doesn't just score risk; it explains *why* (e.g. low attendance, late assignments, fee delinquency) and recommends *what to do* (peer tutoring, financial aid referral, counselling).
4. **Responsible AI:** EduGuard enforces human-in-the-loop governance. Predictions are support guides, protecting student dignity while empowering advisors to act when it matters most.
