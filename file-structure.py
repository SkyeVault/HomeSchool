import os

# Define the base homeschool directory
home_school_path = "HomeSchool"

# Define grade levels
grade_levels = [
    "0-4 Years", "PreK", "Kindergarten"
] + [f"Grade {i}" for i in range(1, 13)]

# Define subjects for each grade level
subjects = [
    "Math",
    "Science",
    "Language Arts",
    "History",
    "Geography",
    "Technology",
    "Engineering",
    "Coding",
    "Music",
    "Art",
    "Home Economics",
    "Physical Education"
]

# Create grade-level folders and subject folders
for grade in grade_levels:
    grade_path = os.path.join(home_school_path, grade)
    os.makedirs(grade_path, exist_ok=True)  # Create grade folder
    
    # Create subject folders within each grade
    for subject in subjects:
        subject_path = os.path.join(grade_path, subject)
        os.makedirs(subject_path, exist_ok=True)

        # Create an empty README.md file in each subject folder
        readme_path = os.path.join(subject_path, "README.md")
        with open(readme_path, "w") as f:
            f.write("")  # Empty file placeholder

        print(f"Created {readme_path}")