# Function to calculate the number of students needing accommodation
def students_needing_accommodation(students):
    return sum(1 for student in students if bool(student["needs_accommodation"]))


# Function to get a list of students with work experience more than 2 years
def students_with_experience(students):
    return [student["first_name"] + ' ' + student["last_name"] for student in students if int(student["work_experience"]) > 2]


# Function to get a list of students who graduated from a technical school
def students_from_technical_school(students):
    return [student["first_name"] + ' ' + student["last_name"] for student in students if student["degree"] == 'Technical School']


# Function to get a list of unique languages studied by students
def unique_languages(students):
    return list(set(student["language"] for student in students))
