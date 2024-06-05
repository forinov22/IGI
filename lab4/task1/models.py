class Person:
    type = "Person"

    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class PersonMixin:
    def display_info(self: Person):
        print(f"Name: {self.first_name}")
        print(f"Surname: {self.last_name}")
        print(f"Age: {self.age}")


class Student(Person, PersonMixin):
    type = "Student"

    def __init__(self, first_name, last_name, age, needs_accommodation, experience, degree, language):
        super().__init__(first_name, last_name, age)
        self.needs_accommodation = needs_accommodation
        self._work_experience = experience
        self.degree = degree
        self.language = language

    # Getter and setter for work experience
    def _get_work_experience(self):
        return self._work_experience

    def _set_work_experience(self, value):
        if value < 0:
            raise ValueError("Work experience cannot be negative.")
        self._work_experience = value

    def _del_work_experience(self):
        del self._work_experience

    work_experience = property(fget=_get_work_experience,
                               fset=_set_work_experience,
                               fdel=_del_work_experience,
                               doc="Work Experience")

    @property
    def full_name(self):
        return (f"First name: {self.first_name}\n"
                f"Last name: {self.last_name}")

    def __str__(self):
        return (f"Name: {self.first_name}, Surname: {self.last_name}, Age: {self.age}, Needs Accommodation: "
                f"{self.needs_accommodation}, Work Experience: {self.work_experience}, Degree: {self.degree}, Language: {self.language}")

    def __repr__(self):
        attributes = [f"\'{key}\': \'{value}\'" for key, value in self.__dict__.items()]
        return '{' + ", ".join(attributes) + '}'
