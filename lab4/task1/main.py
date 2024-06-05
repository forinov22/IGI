from models import Student
from serializers import (write_to_csv,
                         write_to_pickle,
                         read_from_csv,
                         read_from_pickle)
from individual_tasks import (students_needing_accommodation,
                              students_with_experience,
                              students_from_technical_school,
                              unique_languages)


if __name__ == "__main__":
    # Sample student data
    students_data = [
        Student("John", "Doe", 20, True, 3, "Bachelor's", "English"),
        Student("Jane", "Smith", 22, False, 1, "Technical School", "French"),
        Student("Alice", "Johnson", 21, True, 0, "Master's", "Spanish")
    ]

    # Writing data to CSV and pickle files
    write_to_csv("students.csv", students_data)
    write_to_pickle("students.pickle", students_data)

    # Reading data from files
    students_from_csv = read_from_csv("students.csv")
    students_from_pickle = read_from_pickle("students.pickle")

    # print(students_from_csv)
    # print(students_from_pickle)

    # Calculating and displaying results
    print("Number of students needing accommodation:", students_needing_accommodation(students_from_csv))
    print("Students with work experience more than 2 years:", students_with_experience(students_from_csv))
    print("Students graduated from technical school:", students_from_technical_school(students_from_csv))
    print("Unique languages studied by students:", unique_languages(students_from_csv))

