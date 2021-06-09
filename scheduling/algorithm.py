from numpy.core.fromnumeric import shape
from numpy.core.multiarray import empty_like
from data import Class, Student, Teacher
import numpy as np
import random


class Schedule:
    def __init__(self, amount_of_classes_per_day, amount_of_days_per_cicle):
        self.classes = amount_of_classes_per_day
        self.days = amount_of_days_per_cicle
        self.subjects = 9
        self.schedule = self.empty_schedule()

    def empty_schedule(self):
        return np.empty((self.days, self.classes, self.subjects), dtype=object)

    def can_add(self, schedule, key, day_indx, period_indx):
        if key in schedule[day_indx-1][period_indx-1]:
            print(f"Cannot add class: {key.subject_name} {key.teacher.name}; {period_indx}:{day_indx}.")
            return False
        return True

    def add_class(self, schedule, key, day_indx, period_indx):
        for i in range(self.subjects):
            if schedule[day_indx-1][period_indx-1][i] == None:
                schedule[day_indx-1][period_indx-1][i] = key
                return schedule

    def print_schedule(self, schedule, teacher=None, student=None):
        for day in range(self.days):
            print("Day: ", day+1)
            for period in range(self.classes):
                line = f"     Periode {period+1}: "
                for i in schedule[day][period]:
                    if i != None:
                        line += str(i.subject_name) + " "
                print(line)
            

class GeneticAlgorithm(Schedule):
    def __init__(self, pop_size, generation_length, all_keys, amount_of_classes_per_day, amount_of_days_per_cicle):
        Schedule.__init__(self, amount_of_classes_per_day, amount_of_days_per_cicle)
        self.pop_size = pop_size
        self.generation_length = generation_length
        self.all_keys = all_keys
        self.population = self.initial_population()
        
    def initial_population(self):
        population = []
        for i in range(1, self.pop_size+1):
            schedule = self.empty_schedule()
            for key in self.all_keys:
                can_add = False
                while not can_add:
                    rand_day = random.randint(0, self.days-1)
                    rand_class = random.randint(0, self.classes-1)
                    can_add = self.can_add(schedule, key, rand_day, rand_class)
                schedule = self.add_class(schedule, key, rand_day, rand_class)
            print("Index: ", i)
            self.print_schedule(schedule)
        population.append(schedule)
        return population


if True:
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
    eng_key2 = Class(talita, [beans, yeet])
    afr_key1 = Class(karinna, [johan, beans, yeet])
    afr_key2 = Class(karinna, [johna, reagan])
    igo_key1 = Class(scholly, [yeet, beans, bruh])
    igo_key2 = Class(scholly, [johan, reagan])
    wisk_key1 = Class(elsa, [johna, johan])
    wisk_key2 = Class(hellerle, [bruh, yeet, reagan])
    it_key1 = Class(kalli, [johna, reagan, johan, bruh, beans])
    all_keys = [eng_key1, eng_key2, afr_key1, afr_key2, igo_key1, igo_key2, wisk_key1, wisk_key2, it_key1]


    ga = GeneticAlgorithm(pop_size=5, generation_length=5, all_keys=all_keys, amount_of_classes_per_day=2, amount_of_days_per_cicle=2)
