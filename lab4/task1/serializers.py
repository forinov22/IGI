import pickle
import csv


# Function to write student data to a CSV file
def write_to_csv(filename, students):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['first_name', 'last_name', 'age', 'needs_accommodation', 'work_experience', 'degree',
                         'language'])
        for student in students:
            writer.writerow([student.first_name, student.last_name, student.age, student.needs_accommodation,
                             student.work_experience, student.degree, student.language])


# Function to read student data from a pickle file
def read_from_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)


# Function to write student data to a pickle file
def write_to_pickle(filename, students):
    with open(filename, 'wb') as file:
        pickle.dump(students, file)


# Function to read student data from a pickle file
def read_from_pickle(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)
