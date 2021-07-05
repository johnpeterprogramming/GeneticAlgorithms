import numpy as np
import random
import copy

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

        self.key = students[0].name #key 'n beter solution later sodat jy nie hoef te se watse key iets is nie
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
    def __init__(self, classes_per_day, days_per_cicle):
        self.classes_per_day = classes_per_day
        self.days_per_cicle = days_per_cicle
        self.teacher_count = Teacher.count
        self.schedule = self.empty_schedule()

    def empty_schedule(self):
        return np.empty((self.days_per_cicle, self.classes_per_day, self.teacher_count), dtype=object)

    def add_class(self, key, day_indx, period_indx):
        for i in range(self.teacher_count):
            if self.schedule[day_indx-1][period_indx-1][i] == None:
                self.schedule[day_indx-1][period_indx-1][i] = key
                break

    def print_schedule(self, teacher=None, student=None): #Add feature to print schedule for specific student or teacher
        for day in range(self.days_per_cicle):
            print("Day: ", day+1)
            for period in range(self.classes_per_day):
                line = f"     Periode {period+1}: "
                for i in self.schedule[day][period]:
                    if i != None:
                        line += f"{i.subject_name}-{i.teacher.name}, "
                print(line)

    def get_class_count_of_day(self, key, day_indx):
        count = 0
        for period in self.schedule[day_indx]:
            count += np.count_nonzero(period == key)
        return count

class GeneticAlgorithm:
    def __init__(self, pop_size, max_gen_length, all_keys, classes_per_day, days_per_cicle):
        self.days_per_cicle = days_per_cicle
        self.classes_per_day = classes_per_day
        self.pop_size = pop_size
        self.max_gen_length = max_gen_length
        self.all_keys = all_keys
        self.population = self.initial_population()

    def initial_population(self):
        population = []
        insert_chance = .8
        for _ in range(self.pop_size):
            schedule = Schedule(self.classes_per_day, self.days_per_cicle)
            for day in range(self.days_per_cicle):
                for period in range(self.classes_per_day):
                    for _ in range(Teacher.count):
                        rand = random.random()
                        if rand < insert_chance:
                            key = random.choice(self.all_keys)
                            schedule.add_class(key, day, period)

            population.append(schedule)
        return population

    def cal_fitness(self, schedule): #Takes in ARRAY not object
        #Periods of same subject should be double periods
        #Important subjects like maths and science should be in the first 4 periods of the day 

        #Kry die collision count
        collision_count = 0
        for day in range(self.days_per_cicle): 
            for period in range(self.classes_per_day):
                collision_list = list()
                for i in schedule[day][period]:
                    if i == None:
                        continue
                    if i not in collision_list:
                        collision_list.append(i.teacher.name)

                # line = "" #print collision_set
                # for i in collision_list:
                #     line += f"{i.subject_name}-{i.name}; "
                # print(line)

                period_length = 0
                for i in schedule[day][period]:
                    if i:
                        period_length += 1
                collision_count += (period_length - len(set(collision_list)))

        if collision_count != 0:
            collision_fitness = 1/collision_count
        else:
            collision_fitness = 9999 #high number

        return collision_fitness

    def rank_by_fitness(self):
        fitnesses = []
        for sched in self.population:
            fitnesses.append(self.cal_fitness(sched.schedule))
        # print(f"Highest fitness in ranked func: {max(fitnesses)}")

        zipped_pop = [i for i in reversed(sorted(zip(fitnesses, range(self.pop_size))))]
        temp = copy.deepcopy(self.population)
        indx = 0
        for _,j in zipped_pop:
            self.population[indx] = temp[j]
            indx += 1

    def crossover(self, parent1, parent2): #Takes in OBJECT not array
        par1 = copy.deepcopy(parent1)
        par2 = copy.deepcopy(parent2)
        crossover_point = Teacher.count // 2
        for day in range(self.days_per_cicle):
            for period in range(self.classes_per_day):
                par1.schedule[day][period][:crossover_point] = par2.schedule[day][period][:crossover_point]
                par2.schedule[day][period][:crossover_point] = parent1.schedule[day][period][:crossover_point]
        return par1, par2

    def mutation(self, mutant): #Takes in OBJECT
        mutation_rate = 0.7
        remove_rate = 0.7
        if random.random() < mutation_rate:
            rand_day = random.randint(0, self.days_per_cicle-1)
            rand_class = random.randint(0, self.classes_per_day-1)
            rand_indx = random.randint(0, Teacher.count-1)

            mutant.schedule[rand_day][rand_class][rand_indx] = random.choice(self.all_keys)

        if random.random() < remove_rate:
            rand_day = random.randint(0, self.days_per_cicle-1)
            rand_class = random.randint(0, self.classes_per_day-1)
            rand_indx = random.randint(0, Teacher.count-1)
            mutant.schedule[rand_day][rand_class][rand_indx] == None


    def start(self):
        for gen in range(self.max_gen_length):

            crossovers = list()
            for i in range(self.pop_size//2):
                par1, par2 = self.crossover(self.population[i], self.population[(i+1)%self.pop_size])
                crossovers.append(par1)
                crossovers.append(par2)
            
            for mutant in crossovers:
                self.mutation(mutant)

            self.rank_by_fitness()

            best_fitness = self.cal_fitness(self.population[0].schedule)
            print(f"Best fitness at generation {gen}: {best_fitness}")
            
            if best_fitness > 1:
                print("BEST FITNESS ACHIEVED!")
                self.population[0].print_schedule()
                break
                

            self.population[self.pop_size//2:] = crossovers[:self.pop_size//2]


#initialize data from database
if True:
    talita = Teacher("Talita", "eng")
    scholly = Teacher("Scholly", "igo")
    hellerle = Teacher("Hellerle", "wisk")
    kalli = Teacher("Kalli", "it")
    herman = Teacher("Herman", "wetenskap")
    elsa = Teacher("Elsa", "wisk")
    karinna = Teacher("JGert", "afr")

    johna = Student("Johna")
    reagan = Student("Reagan")
    johan = Student("Johan") 
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

ga = GeneticAlgorithm(pop_size=30, max_gen_length=150, all_keys=all_keys, classes_per_day=2, days_per_cicle=2)
ga.start()
ga.rank_by_fitness()
ga.population[0].print_schedule()
