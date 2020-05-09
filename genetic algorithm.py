'''This program finds the global minimum Rastrigin function
f(x1, x2) = 10*2 + ((x1^2 - 10 * cos(2 * pi * x1)) + (x2^2 - 10 * cos(2 * pi * x2)))
х1 = [-5.12; 5.12], х2 = [-5.12; 5.12]
using a genetic algorithm. Individuals (chromosomes) - variables х1 and х2 encoded in binary code and connected in one line'''
import math
import random
import time
import os

x1_min = -5.12
x1_max = 5.12
x2_min = -5.12
x2_max = 5.12

#A variable that takes the number of individuals in a generation
quantity_of_chrom = int(input('Enter the number of individuals (chromosomes): '))
#A variable that takes the probability of a gene mutation from a general population.
probability_of_mutation = float(input('Enter mutation probability: '))

def exponent_m(x_min, x_max):
    '''
    Function to determine the number of bits for each variable.
    :param x_min: variable minimum
    :param x_max: variable maximum
    :return: m - the number of bits for encoding a variable
    '''
    m = (x_max - x_min)*10**5 #10^5 because our chosen accuracy is 5 decimal places
    m = math.log(m, 2)
    m = math.ceil(m)
    return m

def chromosomeGenerator(m1, m2, quantity_of_chrom):
    '''
    Function for encoding variables with binary code
    :param m1: the number of bits for encoding a variable х1
    :param m2: the number of bits for encoding a variable х2
    :param quantity_of_chrom: the number of individuals (chromosomes) in the population entered by the user
    :return: list of randomly generated encoded variables - first generation
    '''
    random_gen1 = ''
    random_gen2 = ''
    population = []
    for i in range(quantity_of_chrom):
        for j in range(m1):
            gen = random.randint(0, 1)
            gen = str(gen)
            random_gen1 += gen

        for j in range(m2):
            gen = random.randint(0, 1)
            gen = str(gen)
            random_gen2 += gen

        chromosome = random_gen1 + random_gen2
        population.append(chromosome)
        random_gen1 = ''
        random_gen2 = ''
    return population

def decoder(population, x1_min, x1_max, x2_min, x2_max, m1, m2):
    '''
    Function for decoding a binary individual (chromosome) to decimal.
    :param population: list of encoded individuals (chromosomes)
    :param x1_min: х1 variable minimum
    :param x1_max: х1 variable maximum
    :param x2_min: х2 variable minimum
    :param x2_max: х2 variable maximum
    :param m1: the number of bits for encoding a variable х1
    :param m2: the number of bits for encoding a variable х2
    :return: list of decoded individuals (chromosomes) [x1, x2]
    '''
    population_dec = []
    for i in range(len(population)):
        chromosome = population[i]
        bin_x1 = chromosome[:m1]
        bin_x2 = chromosome[m1:]
        dec_x1 = int(bin_x1, 2)
        dec_x2 = int(bin_x2, 2)
        x1 = x1_min + dec_x1 * (x1_max - x1_min) / (2 ** m1 - 1)
        x2 = x2_min + dec_x2 * (x2_max - x2_min) / (2 ** m2 - 1)
        x1 = round(x1, 5)
        x2 = round(x2, 5)
        population_dec.append([x1, x2])
    return population_dec

#целевая функция
def eval_function(population_dec):
    '''
    Function to calculate the value of a function
    :param population_dec: list of individuals (chromosomes) in decimal form
    :return: list of function values for each individual (chromosome)
    '''
    eval_list = []
    for i in range(len(population_dec)):
        x1 = population_dec[i][0]
        x2 = population_dec[i][1]
        f = -(10*2 + ((x1**2 - 10 * math.cos(2 * math.pi * x1)) + (x2**2 - 10 * math.cos(2 * math.pi * x2)))) #Rastrigin function
        f = round(f, 5)
        eval_list.append(f)
    return eval_list

def cumulative_probability(eval_list):
    '''
    Function for calculating the cumulative probability for a population
    :param eval_list: list of function values for each individual (chromosome)
    :return: list of aggregate population probabilities
    '''
    f = 0
    probability_list = []
    q = 0
    cumulative_probability_list = []
    for i in eval_list:
        f += i - min(eval_list) #general matching function
    for i in eval_list:
        if f != 0:
            p = ((i - min(eval_list))/f)    #probability of selection of each chromosome
        else:
            p = 1 / len(eval_list)
        probability_list.append(p)
    for i in probability_list:
        q += i #cumulative probability
        cumulative_probability_list.append(q)
    return cumulative_probability_list

def roulette_wheel(population, q_list):
    '''
    Function to implement the "roulette wheel" approach for selecting individuals for a new population.
    :param population: list of encoded individuals (chromosomes)
    :param q_list: list of aggregate population probabilities
    :return: list of selected individuals (chromosomes)
    '''
    new_population = []
    for i in range(len(population)):
        r = random.random()
        for j in range(len(population)):
            if r <= q_list[j]:
                new_population.append(population[j])
                break
    return new_population

def crossbreeding(population):
    '''
    Function for crossing randomly selected individuals
    :param population: list of encoded individuals (chromosomes) after selection
    :return: a list of a new population in which some individuals (chromosomes) were crossed among themselves
    '''
    cross_population = []
    index_list = []
    rand_position = random.randint(1, len(population[0])-1)
    new_cross_population = []

    for i in range(len(population)):
        r = random.random()
        if r < 0.25:  # cross chance
            cross_population.append(population[i])
            index_list.append(i)
    # crossing selected chromosomes
    m = len(cross_population)
    if m > 1:
        for i in range(0, len(cross_population) - 1, 2):
            parent1 = cross_population[i]
            parent2 = cross_population[i + 1]
            chrom1 = parent1[:rand_position] + parent2[rand_position:]
            chrom2 = parent2[:rand_position] + parent1[rand_position:]
            new_cross_population.append(chrom1)
            new_cross_population.append(chrom2)
        new_cross_population.append(cross_population[len(cross_population) - 1])
        # replacement of chromosomes with crossed
        j = 0
        for i in index_list:
            population[i] = new_cross_population[j]
            j += 1
    return population

def mutation(population, probability_of_mutation):
    '''
    Function for mutating random genes (bits) from the entire population
    :param population: list of encoded individuals (chromosomes) after selection and crossing
    :param probability_of_mutation: probability of a gene mutation from a general population
    :return: list of cached individuals (chromosomes) after mutation
    '''
    chrom_len = len(population[0])
    quantity_gen = chrom_len * len(population)
    index_gen = []
    for i in range(1, quantity_gen):
        r = random.random()
        if r < probability_of_mutation:
            index_gen.append(i)
    for i in index_gen:
        number_chrom = i // chrom_len
        gen_in_chrom = i % chrom_len - 1
        if gen_in_chrom == -1:
            number_chrom -= 1
            gen_in_chrom = chrom_len - 1
        chromosome = population[number_chrom]
        gen = chromosome[gen_in_chrom]
        if gen == '0':
            gen = '1'
        else:
            gen = '0'
        mut_chrom = chromosome[:gen_in_chrom] + gen + chromosome[gen_in_chrom + 1:]
        population[number_chrom] = mut_chrom
    return population

def prog(x1_min, x1_max, x2_min, x2_max, quantity_of_chrom, probabiliti_of_mutation):
    '''
    main function
    :param x1_min: х1 variable minimum
    :param x1_max: х1 variable maximum
    :param x2_min: х2 variable minimum
    :param x2_max: х2 variable maximum
    :param quantity_of_chrom: the number of individuals (chromosomes) in the population entered by the user
    :param probabiliti_of_mutation: probability of a gene mutation from a general population
    :return: result of the work of the whole program
    '''
    start_time = time.time()
    m1 = exponent_m(x1_min, x1_max)
    m2 = exponent_m(x2_min, x2_max)
    first_population = chromosomeGenerator(m1, m2, quantity_of_chrom)
    population = list(first_population)
    best_chrom_list =[]
    n = 1000 # number of iterations
    for i in range(n):
        population_dec = decoder(population, x1_min, x1_max, x2_min, x2_max, m1, m2)
        eval_list = eval_function(population_dec)

        index_best_chrom = eval_list.index(max(eval_list))
        best_chrom = population_dec[index_best_chrom]
        best_chrom_list.append([max(eval_list), best_chrom, i+1])

        q_list = cumulative_probability(eval_list)
        select_pop = roulette_wheel(population, q_list)
        population = list(select_pop)
        crross_pop = crossbreeding(population)
        population = list(crross_pop)
        mut_pop = mutation(population, probabiliti_of_mutation)
        population = list(mut_pop)

    time_of_work = (time.time() - start_time)
    time_of_work = round(time_of_work, 5)
    best_of_the_best = max(best_chrom_list)
    print('\nThe best individual - {0}, was received in {1} generation. The value of the objective function - {2}'.format(best_of_the_best[1], best_of_the_best[2], best_of_the_best[0]))
    print('Number of individuals per generation: {0}; mutation probability: {1}'.format(quantity_of_chrom, probabiliti_of_mutation))
    print('Program runtime: {0} seconds'.format(time_of_work))

prog(x1_min, x1_max, x2_min, x2_max, quantity_of_chrom, probability_of_mutation)
os.system("pause")