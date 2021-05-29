import numpy as np
import random

# item_weight = np.random.randint(1, 15, size = item_count)
# item_value = np.random.randint(10, 750, size = item_count)

items = ['cap', 'socks', 'mug', 'bottle', 'tissues', 'notepad', 'laptop', 'headphones', 'mints', 'phone']
item_weight = np.array([70, 38, 350, 192, 80, 333, 2200, 160, 25, 200])
item_value = np.array([100, 10, 60, 30, 15, 40, 500, 150, 5, 500])
item_count = item_weight.shape[0]

max_weight = 3000


solutions_per_pop = 15
pop_size = (solutions_per_pop, item_count)
population = np.random.randint(2, size = pop_size)
num_generations = 100

def fitness_calc(pop):
    fitness = np.zeros(pop.shape[0])
    for i in range(pop.shape[0]):
        values = np.sum(item_value * pop[i])
        weight = np.sum(item_weight * pop[i])

        if weight <= max_weight:
            fitness[i] = values
    return fitness.astype(int)

def selection(pop):
    fitness = fitness_calc(pop)
    parents = np.empty(pop_size)
    for i in range(parents.shape[0]):
        best_fitness_index = np.where(fitness == np.max(fitness))
        parents[i] = pop[best_fitness_index[0][0]]
        fitness[best_fitness_index[0][0]] = -1
    return parents.astype(int)

def crossover(pop):
    crossover_point = pop.shape[1] // 2
    new_arr = np.empty(pop.shape)
    num_offsprings = pop.shape[0]
    for i in range(num_offsprings):
        index2 = (i+1)%num_offsprings
        new_arr[i][:crossover_point] = pop[i][:crossover_point] #behou eerste helfte
        new_arr[i][crossover_point:] = pop[index2][crossover_point:] #einde helfte

    return new_arr.astype(int)

def mutation(pop):
    mutation_rate = 0.7
    for i in range(pop.shape[0]):
        if random.random() < mutation_rate:
            random_index = random.randint(0, pop.shape[1]-1)
            pop[i][random_index] = abs(pop[i][random_index] - 1) # verander 1 na 0  en  0 na 1
    return pop

print("INITIAL POPULATION")
print(population)

for gen in range(num_generations):
    fitness = fitness_calc(population)
    selected_parents = selection(population)

    best_fitness = np.max(fitness)

    average = round(np.average(fitness), 2)
    print(f"Gen({gen}): Average: {average}, Best: {best_fitness}")

    children = crossover(selected_parents)
    mutants = mutation(children)

    combination_index = population.shape[0] // 2

    population[:combination_index] = selected_parents[:combination_index] #HOu helfte van die origonal parents en add die children
    population[combination_index:] = mutants[combination_index:]



print(f"Best fitness after {gen} generations: {best_fitness}")
print(selected_parents[0])

for i in range(item_count):
    if selected_parents[0][i] == 1:
        print(items[i])
