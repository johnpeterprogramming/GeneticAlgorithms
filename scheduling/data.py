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

class Class: #Ek moet hierdie later 'n child maak van die Teacher class maak perhaps
    def __init__(self, teacher, students):
        self.subject_name = teacher.subject_name
        self.students = students
        self.teacher = teacher

        for student in self.students:
            student.classes.append(self)
        self.teacher.classes.append(self)


class Teacher:
    def __init__(self, name, subject_name):
        self.classroom_size = 30
        self.name = name
        self.subject_name = subject_name

        self.classes = list()



talita = Teacher("Talita", "eng")
scholly = Teacher("Scholly", "igo")
hellerle = Teacher("Hellerle", "wisk")
kalli = Teacher("Kalli", "it")
herman = Teacher("Meneer Herman", "wetenskap")
elsa = Teacher("Elsa van Zyl", "wisk")
hellerle = Teacher("Hellerle", "wisk")
karinna = Teacher("Juf Gert", "afr")

johna = Student("John-Peter Krause")
reagan = Student("Reagan Botha")
johan = Student("Johan Bruh") 
bruh = Student("Bruh")
beans = Student("Beans")
yeet = Student("Yeet") 

eng_key1 = Class(talita, [johna, reagan, bruh])
eng_key2 = Class(talita, [johan, beans, yeet])

afr_key1 = Class(karinna, [johan, beans, yeet])
afr_key2 = Class(karinna, [johna, reagan, bruh])

igo_key1 = Class(scholly, [johna, yeet, beans, bruh])
igo_key2 = Class(scholly, [johan, reagan])

wisk_key1 = Class(elsa, [johna, johan])
wisk_key2 = Class(hellerle, [bruh, beans, yeet, reagan])

it_key1 = Class(kalli, [johna, reagan, johan, bruh, beans, yeet])

all_keys = [eng_key1, eng_key2, afr_key1, afr_key2, igo_key1, igo_key2, wisk_key1, wisk_key2, it_key1]

for key in all_keys:
    print(f"Subject: {key.subject_name}")
    for student in key.students:
        print(f"Student: {student.name}")

    print()

