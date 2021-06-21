import numpy as np
import random

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
    def __init__(self, teacher, students, key):
        Class.count += 1

        self.key = key #key 'n beter solution later sodat jy nie hoef te se watse key iets is nie
        self.subject_name = teacher.subject_name
        self.students = students
        self.teacher = teacher

class Teacher:
    count = 0
    def __init__(self, name, subject_name):
        Teacher.count += 1
        self.classroom_size = 5
        self.name = name
        self.subject_name = subject_name

        self.classes = list()

class Schedule:
    def __init__(self, amount_of_classes_per_day, amount_of_days_per_cicle):
        self.period_count = amount_of_classes_per_day
        self.days = amount_of_days_per_cicle
        self.teacher_count = Teacher.count
        self.schedule = self.empty_schedule()

    def empty_schedule(self):
        return np.empty((self.days, self.period_count, self.teacher_count), dtype=object)

    def add_class(self, schedule, key, day_indx, period_indx):
        for i in range(self.teacher_count):
            if schedule[day_indx-1][period_indx-1][i] == None:
                schedule[day_indx-1][period_indx-1][i] = key
                return schedule

    def print_schedule(self, schedule, teacher=None, student=None): #Add feature to print schedule for specific student or teacher
        for day in range(self.days):
            print("Day: ", day+1)
            for period in range(self.period_count):
                line = f"     Periode {period+1}: "
                for i in schedule[day][period]:
                    if i != None:
                        line += f"{i.subject_name}{i.key}-{i.teacher.name}, "
                print(line)

    def get_class_count_of_day(self, schedule, key, day_indx):
        count = 0
        for period in schedule[day_indx]:
            count += np.count_nonzero(period == key)
        return count

class GeneticAlgorithm(Schedule):
    def __init__(self, pop_size, generation_length, all_keys, amount_of_classes_per_day, amount_of_days_per_cicle):
        Schedule.__init__(self, amount_of_classes_per_day, amount_of_days_per_cicle)
        self.pop_size = pop_size
        self.generation_length = generation_length
        self.all_keys = all_keys
        self.population = self.initial_population()
        
    def initial_population(self):
        population = []
        insert_chance = 0.8 #ek dink dit moet af hang van die vak??
        for _ in range(1, self.pop_size+1):
            schedule = self.empty_schedule()
            for day in range(self.days):
                for period in range(self.period_count):
                    for _ in range(self.teacher_count):
                        rand = random.random()
                        if rand < insert_chance:
                            key = random.choice(self.all_keys)
                            schedule = self.add_class(schedule, key, day, period)

        population.append(schedule)
        return population

    def cal_fitness(self, schedule):
        #Periods of same subject should be double periods
        #Distance between classes should be minimal
        #Important subjects like maths and science should be in the first 4 periods of the day 

        #Kry die collision count
        collision_count = 0
        for day in range(self.days): 
            for period in range(self.period_count):
                collision_set = set(schedule[day][period])
                if None in collision_set:
                    collision_set.remove(None)
                # line = "" #print collision_set
                # for i in collision_set:
                #     line += f"{i.subject_name}{i.teacher_class_id}-{i.teacher.name}; "
                # print(line)

                period_length = 0
                for i in schedule[day][period]:
                    if i:
                        period_length += 1
                collision_count += period_length - len(collision_set)

        print("Collision count: ", collision_count)
        if collision_count != 0:
            collision_fitness = 1/collision_count
        else:
            collision_fitness = 69 #high number

        #No more than 2 periods of same subject per day
        for key in self.all_keys:
            count = 0
            for day in range(self.days):
                count += self.get_class_count_of_day(schedule, key, day)
            print(f"{key.teacher.name}{key.key}: {count}")


        return collision_fitness,


#initialize data from database
if True:
    talita = Teacher("Talita", "eng")
    scholly = Teacher("Scholly", "igo")
    hellerle = Teacher("Hellerle", "wisk")
    kalli = Teacher("Kalli", "it")
    herman = Teacher("Herman", "wetenskap")
    elsa = Teacher("Elsa", "wisk")
    karinna = Teacher("JGert", "afr")

    johna = Student("John-Peter Krause")
    reagan = Student("Reagan Botha")
    johan = Student("Johan Bruh") 
    bruh = Student("Bruh")
    beans = Student("Beans")
    yeet = Student("Yeet") 

    eng_key1 = Class(talita, [johna, reagan, bruh], 1)
    eng_key2 = Class(talita, [beans, yeet], 2)
    afr_key1 = Class(karinna, [johan, beans, yeet], 1)
    afr_key2 = Class(karinna, [johna, reagan], 2)
    igo_key1 = Class(scholly, [yeet, beans, bruh], 1)
    igo_key2 = Class(scholly, [johan, reagan], 2)
    wisk_key1 = Class(elsa, [johna, johan], 1)
    wisk_key2 = Class(hellerle, [bruh, yeet, reagan], 2)
    it_key1 = Class(kalli, [johna, reagan, johan, bruh, beans], 1)
    all_keys = [eng_key1, eng_key2, afr_key1, afr_key2, igo_key1, igo_key2, wisk_key1, wisk_key2, it_key1]

ga = GeneticAlgorithm(pop_size=1, generation_length=1, all_keys=all_keys, amount_of_classes_per_day=2, amount_of_days_per_cicle=2)

test_pop = ga.population[0]
ga.print_schedule(test_pop)
print(ga.cal_fitness(test_pop))


