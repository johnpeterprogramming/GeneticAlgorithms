from os import sched_get_priority_max
from data import Class, Student, Teacher
import numpy as np


class Schedule:
    def __init__(self, amount_of_classes_per_day, amount_of_days_per_cicle, amount_of_keys):
        self.classes = amount_of_classes_per_day
        self.days = amount_of_days_per_cicle
        self.subjects = amount_of_keys
        self.schedule = np.empty((self.days, self.classes, self.subjects), dtype=object)


    def check_conflicts(self):
        pass

    def add_class(self, key, period_indx, day_indx):
        for i in range(self.subjects):
            if self.schedule[day_indx-1][period_indx-1][i] == None:
                self.schedule[day_indx-1][period_indx-1][i] = key
                break

    def get_class(self):
        pass

    def print_schedule(self, teacher=None, student=None):
        for day in range(self.days):
            print("Day: ", day+1)
            for period in range(self.classes):
                line = f"     Periode {period+1}: "
                for i in self.schedule[day][period]:
                    if i != None:
                        line += str(i.subject_name) + " "
                print(line)
            

class GenteticAglotithm:
    def __init__(self, pop_size, generation_length):
        pass

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
    # igo_key1 = Class(scholly, [yeet, beans, bruh])
    # igo_key2 = Class(scholly, [johan, reagan])
    # wisk_key1 = Class(elsa, [johna, johan])
    # wisk_key2 = Class(hellerle, [bruh, yeet, reagan])
    # it_key1 = Class(kalli, [johna, reagan, johan, bruh, beans])
    # all_keys = [eng_key1, eng_key2, afr_key1, afr_key2, igo_key1, igo_key2, wisk_key1, wisk_key2, it_key1]

    schedule = Schedule(amount_of_classes_per_day=9, amount_of_days_per_cicle=6, amount_of_keys=Class.amount_of_subjects)
    schedule.add_class(eng_key1, period_indx= 1, day_indx= 1)
    schedule.add_class(eng_key1, period_indx= 2, day_indx= 2)
    schedule.add_class(afr_key2, period_indx= 3, day_indx= 2)
    schedule.add_class(afr_key2, period_indx= 3, day_indx= 2)
    schedule.add_class(afr_key2, period_indx= 3, day_indx= 2)
    schedule.print_schedule()
