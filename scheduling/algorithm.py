from data import Class, Student, Teacher
import numpy as np
import random


class Schedule:
    def __init__(self, amount_of_classes_per_day, amount_of_days_per_cicle):
        self.period_count = amount_of_classes_per_day
        self.days = amount_of_days_per_cicle
        self.teacher_count = Teacher.count
        self.schedule = self.empty_schedule()

    def empty_schedule(self):
        return np.empty((self.days, self.period_count, self.teacher_count), dtype=object)

    def can_add(self, schedule, key, day_indx, period_indx):
        if key in schedule[day_indx-1][period_indx-1]:
            print(f"Cannot add class: {key.subject_name} {key.teacher.name}; {period_indx}:{day_indx}.")
            return False
        return True

    def add_class(self, schedule, key, day_indx, period_indx):
        for i in range(self.teacher_count):
            if schedule[day_indx-1][period_indx-1][i] == None:
                schedule[day_indx-1][period_indx-1][i] = key
                key.added_to_shedule(day_indx)

                return schedule

    def print_schedule(self, schedule, teacher=None, student=None):
        for day in range(self.days):
            print("Day: ", day+1)
            for period in range(self.period_count):
                line = f"     Periode {period+1}: "
                for i in schedule[day][period]:
                    if i != None:
                        line += f"{i.subject_name}-{i.teacher.name}, "
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
            for day in range(self.days):
                for period in range(self.period_count):
                    for _ in range(self.teacher_count):
                        key = random.choice(self.all_keys)
                        self.add_class(schedule, key, day, period)
                
            # print("Population ", i)
            # self.print_schedule(schedule)
        population.append(schedule)
        return population

    def cal_fitness(self, schedule):
        
        #Periods of same subject should be double periods
        #Distance between classes should be minimal
        #Important subjects like maths and science should be in the first 4 periods of the day

        fitness_score = np.zeros((5)) 

        #Kry die collision count
        collision_count = 0
        for day in range(self.days): 
            for period in range(self.period_count):
                collision_set = set(schedule[day][period])
                # line = ""
                # for i in collision_set:
                #     line += f"{i.subject_name}-{i.teacher.name}; "
                # print(line) Om die collision set uit te print
                collision_count += len(schedule[day][period]) - len(collision_set)

        print("Collision count: ", collision_count)
        fitness_score[0] = 1/collision_count

        #No more than 2 periods of same subject per day
        for key in self.all_keys:
            print(key.teacher.name)
            print(key.days_count)
            print()

        return fitness_score


        
        return fitness
        


if __name__ == "__main__":
    talita = Teacher("Talita", "eng")
    scholly = Teacher("Scholly", "igo")
    hellerle = Teacher("Hellerle", "wisk")
    kalli = Teacher("Kalli", "it")
    herman = Teacher("Herman", "wetenskap")
    elsa = Teacher("Elsa", "wisk")
    hellerle = Teacher("Hellerle", "wisk")
    karinna = Teacher("JGert", "afr")

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


    ga = GeneticAlgorithm(pop_size=2, generation_length=5, all_keys=all_keys, amount_of_classes_per_day=2, amount_of_days_per_cicle=2)
    ga.print_schedule(ga.population[0])
    print(ga.cal_fitness(ga.population[0]))