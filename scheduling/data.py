class Student:
    id = 0
    
    def __init__(self, name):
        Student.id += 1
        self.student_id = Student.id

        self.name = name
        self.classes = list()

    def print_subjects(self):
        print(f"{self.name}'s subjects")
        for i in self.classes:
            print(i.subject_name)
        print()

class Class:
    count = 0
    # class_list = []
    def __init__(self, teacher, students):
        Class.count += 1
        
        self.subject_name = teacher.subject_name
        self.students = students
        self.teacher = teacher

        for student in self.students:
            student.classes.append(self)
        if len(self.teacher.classes) < self.teacher.classroom_size:
            self.teacher.classes.append(self)
        else:
            print("Too much students cringe bruh")

        # Class.class_list.append(self)

class Teacher:
    count = 0
    def __init__(self, name, subject_name):
        Teacher.count += 1
        self.classroom_size = 5
        self.name = name
        self.subject_name = subject_name

        self.classes = list()

#Decode al die inligting van die studente en onderwysers van 'n database af of spreadsheet
def decoder(): 
    pass