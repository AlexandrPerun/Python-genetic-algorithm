'''This program using a genetic algorithm synthesizes a phrase that will correspond to a phrase entered by the user
from a set of letters of the Latin alphabet generated randomly.'''
import random
import time
import os

phrase = input('Enter the phrase (only letters of the Latin alphabet): ')
phrase_clear = ''

# clear the entered phrase from spaces and characters
for i in range(len(phrase)):
    if phrase[i].isalpha() is True:
        phrase_clear += phrase[i]
phrase = phrase_clear
phrase = phrase.lower()

# A variable that takes the number of individuals in a generation
quantity_chrom = int(input('Enter the number of individuals: '))

def chromosomeGenerator(phrase, quantity_chrom):
    '''
    The function generates the first population in the form of the ASKII code of random letters of the Latin alphabet
    :param phrase: phrase entered by the user (to match the length of the individual to the length of the phrase)
    :param quantity_chrom: the number of individuals in the population entered by the user
    :return: first population in the form of a list of numbers - lowercase Latin letter codes from ASKII table
    '''
    population = []
    chrom = []
    for i in range(quantity_chrom):
        for j in range(len(phrase)):
            rand_letter = random.randint(97, 122)
            chrom.append(rand_letter)
        population.append(chrom)
        chrom = []
    return population

def decoder(population):
    '''
    Function for decoding an individual into a string of letters of the Latin alphabet
    :param population: list of randomly generated individuals
    :return: list of decoded individuals - strings
    '''
    population_str = []
    chrom_str = ''
    for chrom in population:
        for letter in chrom:
            letter_str = chr(letter)
            chrom_str += letter_str
        population_str.append(chrom_str)
        chrom_str = ''
    return population_str

def eval_function(phrase, population_str):
    '''
    Function for calculating the correspondence function (correspondence of the generated phrase to the phrase entered by the user)
    :param phrase: phrase entered by the user
    :param population_str: list of decoded individuals - strings
    :return: list of values of the correspondence function for each individual
    '''
    eval_list = []
    eval_func = 0
    for chrom in population_str:
        for i in range(len(phrase)):
            if chrom[i] == phrase[i]:
                eval_func += 1
        eval_list.append(eval_func)
        eval_func = 0
    return eval_list

def cumulative_probability(eval_list):
    '''
    Function for calculating the cumulative probability for a population
    :param eval_list: list of function values for each individual
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
    :param population: list of encoded individuals
    :param q_list: list of aggregate population probabilities
    :return: list of selected individuals
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
        if r < 0.5:  # cross chance
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

def mutation(population):
    '''
    Function for mutating random genes (letter) from the entire population
    :param population: list of encoded individuals after selection and crossing
    :return: list of cached individuals after mutation
    '''
    chrom_len = len(population[0])
    quantity_gen = chrom_len * len(population)
    index_gen = []
    for i in range(1, quantity_gen):
        r = random.random()
        if r < 0.01: # probability of gene mutation
            index_gen.append(i)
    for i in index_gen:
        number_chrom = i // chrom_len
        gen_in_chrom = i % chrom_len - 1
        if gen_in_chrom == -1:
            number_chrom -= 1
            gen_in_chrom = chrom_len - 1
        chromosome = population[number_chrom]
        gen = random.randint(97, 122)
        gen = chr(gen)
        mut_chrom = chromosome[:gen_in_chrom] + gen + chromosome[gen_in_chrom + 1:]
        population[number_chrom] = mut_chrom
    return population

def prog(phrase, quantity_chrom):
    '''
    main function
    :param phrase: phrase entered by the user
    :param quantity_chrom: the number of individuals in the population entered by the user
    :return: result of the work of the whole program
    '''
    start_time = time.time()
    first_pop = chromosomeGenerator(phrase, quantity_chrom)
    population = decoder(first_pop)
    n = 1000 # number of iterations
    for i in range(n):
        population_copy = list(population)
        eval_list = eval_function(phrase, population_copy)

        best_chrom = max(eval_list)
        index_best_chrom = eval_list.index(max(eval_list))
        if best_chrom == len(phrase):
            print('\nThe best individual - {0}, was received in {1} generation.'.format(population_copy[index_best_chrom], i))
            print('The generation in which the best individual was synthesized:', population_copy)
            break

        q_list = cumulative_probability(eval_list)
        select_pop = roulette_wheel(population,q_list)
        select_pop_copy = list(select_pop)
        cross_pop = crossbreeding(select_pop_copy)
        cross_pop_copy = list(cross_pop)
        mut_population = mutation(cross_pop_copy)
        population = list(mut_population)

    if max(eval_list) != len(phrase):
        print('\nThe phrase has not been synthesized. Change the phrase or change the number of individuals')
        print('Last generation:', population)

    time_of_work = (time.time() - start_time)
    time_of_work = round(time_of_work, 3)
    print('Program runtime: {0} seconds\n'.format(time_of_work))

prog(phrase, quantity_chrom)
os.system("pause")