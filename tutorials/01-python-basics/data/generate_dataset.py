"""Generate the university analytics synthetic dataset used across all tutorials.

Run from the project root:
    python tutorials/01-python-basics/data/generate_dataset.py

Produces two files in the same directory:
    university_analytics.csv  -- one row per (student, course) enrollment
    courses.csv               -- one row per course, for join examples
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

OUT_DIR = pathlib.Path(__file__).parent
RNG = np.random.default_rng(42)

# ── Course catalogue ──────────────────────────────────────────────────────────

COURSES = pd.DataFrame(
    {
        "course_id": ["C01", "C02", "C03", "C04", "C05", "C06"],
        "course": [
            "Python Programming",
            "Statistics",
            "Data Structures",
            "Linear Algebra",
            "Machine Learning",
            "Databases",
        ],
        "credits": [3, 3, 4, 3, 4, 3],
        "department": [
            "Computing",
            "Mathematics",
            "Computing",
            "Mathematics",
            "Computing",
            "Computing",
        ],
        "instructor": [
            "Dr. Aiko Tanaka",
            "Prof. Samuel Osei",
            "Dr. Fatima Al-Rashid",
            "Prof. Carlos Mendez",
            "Dr. Priya Nair",
            "Dr. James Kariuki",
        ],
    }
)

# ── Student population ────────────────────────────────────────────────────────

N_STUDENTS = 400
N_COURSES = len(COURSES)

PROGRAMS = ["Computer Science", "Data Science", "Information Technology", "Engineering"]
GENDERS = ["F", "M", "Other"]
REGIONS = ["North", "South", "East", "West", "Central"]
GUARDIANS = ["Father", "Mother", "Sibling", "Other"]
COHORTS = [2022, 2023, 2024]

student_ids = [f"S{i:04d}" for i in range(1, N_STUDENTS + 1)]
programs = RNG.choice(PROGRAMS, size=N_STUDENTS, p=[0.30, 0.35, 0.20, 0.15])
genders = RNG.choice(GENDERS, size=N_STUDENTS, p=[0.48, 0.48, 0.04])
regions = RNG.choice(REGIONS, size=N_STUDENTS)
guardians = RNG.choice(GUARDIANS, size=N_STUDENTS, p=[0.40, 0.38, 0.12, 0.10])
has_internet = RNG.choice([True, False], size=N_STUDENTS, p=[0.78, 0.22])
cohorts = RNG.choice(COHORTS, size=N_STUDENTS)

students = pd.DataFrame(
    {
        "student_id": student_ids,
        "cohort": cohorts,
        "program": programs,
        "gender": genders,
        "region": regions,
        "guardian": guardians,
        "has_internet": has_internet,
    }
)

# ── Enrolments: every student takes every course ──────────────────────────────

SEMESTER_MAP = {
    2022: ["Fall 2022", "Spring 2023"],
    2023: ["Fall 2023", "Spring 2024"],
    2024: ["Fall 2024", "Spring 2025"],
}
SEMESTER_DATES = {
    "Fall 2022": "2022-09-05",
    "Spring 2023": "2023-01-16",
    "Fall 2023": "2023-09-04",
    "Spring 2024": "2024-01-15",
    "Fall 2024": "2024-09-02",
    "Spring 2025": "2025-01-13",
}

rows = []
for _, student in students.iterrows():
    semesters_for_cohort = SEMESTER_MAP[student["cohort"]]
    for i, course_row in COURSES.iterrows():
        semester = semesters_for_cohort[i % 2]

        # Base performance correlated with program and internet access
        program_bonus = {"Computer Science": 3, "Data Science": 4, "Engineering": 2, "Information Technology": 1}[
            student["program"]
        ]
        internet_bonus = 4 if student["has_internet"] else -2

        base = 55 + program_bonus + internet_bonus
        study_hours = float(np.clip(RNG.normal(18, 7), 2, 45))
        study_bonus = (study_hours - 18) * 0.6
        attendance_pct = float(np.clip(RNG.normal(75, 15), 20, 100))
        attendance_bonus = (attendance_pct - 75) * 0.2

        midterm = float(np.clip(RNG.normal(base + study_bonus * 0.5 + attendance_bonus, 12), 10, 100))
        final = float(np.clip(RNG.normal(base + study_bonus + attendance_bonus, 14), 10, 100))
        project = float(np.clip(RNG.normal(base + 5 + study_bonus * 0.3, 10), 10, 100))

        composite = 0.30 * midterm + 0.45 * final + 0.25 * project
        if composite >= 70:
            grade = "A" if composite >= 85 else "B"
        elif composite >= 55:
            grade = "C"
        elif composite >= 45:
            grade = "D"
        else:
            grade = "F"

        # Introduce ~3% missing values on midterm and attendance
        if RNG.random() < 0.03:
            midterm = float("nan")
        if RNG.random() < 0.03:
            attendance_pct = float("nan")

        rows.append(
            {
                "student_id": student["student_id"],
                "cohort": student["cohort"],
                "program": student["program"],
                "gender": student["gender"],
                "region": student["region"],
                "guardian": student["guardian"],
                "has_internet": student["has_internet"],
                "course_id": course_row["course_id"],
                "course": course_row["course"],
                "semester": semester,
                "enrollment_date": SEMESTER_DATES[semester],
                "study_hours": round(study_hours, 1),
                "attendance_pct": round(attendance_pct, 1) if not np.isnan(attendance_pct) else float("nan"),
                "midterm_score": round(midterm, 1) if not np.isnan(midterm) else float("nan"),
                "final_score": round(final, 1),
                "project_score": round(project, 1),
                "final_grade": grade,
                "passed": grade not in ("F",),
            }
        )

df = pd.DataFrame(rows)
df["enrollment_date"] = pd.to_datetime(df["enrollment_date"])

# ── Write outputs ─────────────────────────────────────────────────────────────

df.to_csv(OUT_DIR / "university_analytics.csv", index=False)
COURSES.to_csv(OUT_DIR / "courses.csv", index=False)

print(f"university_analytics.csv: {len(df):,} rows × {df.shape[1]} columns")
print(f"courses.csv:              {len(COURSES)} rows × {COURSES.shape[1]} columns")
print(f"\nColumn dtypes:\n{df.dtypes}")
print(f"\nMissing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
