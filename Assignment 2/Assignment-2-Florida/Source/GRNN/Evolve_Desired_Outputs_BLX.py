import optparse
import collections
import operator
import random
import GRNN_Desired_Outputs

def Evaluate(feature_files,population,sigma):
    fitness = {}
    for key in population:
        accuracy = GRNN_Desired_Outputs.main(feature_files, sigma, population[key])
        error = 1 - accuracy
        fitness[key] = error
    return fitness

def Select_Parents(population,fitness,k):
    k_parents = random.sample(population,k)
    fitness_list = {}
    for parent in k_parents:
        fitness_list[parent] = fitness[parent]
    fitness_sort = collections.OrderedDict(sorted(fitness.items(), key=lambda x: x[1]))
    parents = fitness_sort.items()
    parent_1 = parents[0][0]
    parent_2 = parents[1][0]
    return parent_1, parent_2

def Procreate(population,parent_1,parent_2):
    child_1 = []
    child_2 = []
    for gene in range(0,len(population[parent_1])):
        child_1_gene = random.uniform(population[parent_1][gene],population[parent_2][gene])
        child_1.append(child_1_gene)
        child_2_gene = random.uniform(population[parent_1][gene], population[parent_2][gene])
        child_2.append(child_2_gene)
    return child_1,child_2

def Mutate(pchild_1,pchild_2,sigma):
    child_1 = []
    child_2 = []
    for gene in range(0, len(pchild_1)):
        child_1_gene = pchild_1[gene] + (sigma * random.gauss(0,1))
        child_1.append(child_1_gene)
        child_2_gene = pchild_2[gene] + (sigma * random.gauss(0,1))
        child_2.append(child_2_gene)
    return child_1,child_2

def Select_Survivors(fitness):
    fitness_sort = collections.OrderedDict(sorted(fitness.items(), key=lambda x: x[1],reverse=True))
    worst_individuals = fitness_sort.items()
    worst_1 = worst_individuals[0][0]
    worst_2 = worst_individuals[1][0]
    return worst_1, worst_2

def main():
    # defining the way i want to capture user input
    parser = optparse.OptionParser()
    parser.add_option('--feature_files', dest='feature_files',
                      default='',  # default empty!
                      help='location of feature files')
    parser.add_option('--sigma', dest='sigma',
                      default='',  # default empty!
                      help='sigma value')
    (options, args) = parser.parse_args()

    # assigning the user input
    feature_files = options.feature_files
    sigma = float(options.sigma)

    feature_files = open(feature_files,'r')
    features = feature_files.readlines()

    # get authors
    train_set = []
    authors = []
    for feature in features:
        feature = feature.strip()
        train_set.append(feature)
        feature_list = feature.split(',')
        if feature_list[0] not in authors:
            authors.append(feature_list[0])

    # initialize population
    population_size = 20
    population = {}
    for pop in range(0,population_size):
        desired_vector = []
        for num in range(0,len(authors)):
            desired_vector.append(random.gauss(0,1))
        population[pop] = desired_vector

    # Evaluate Fitness of Initial Population
    fitness = Evaluate(options.feature_files,population,sigma)
    print "Fitness of Initial Population:"
    print fitness

    k = 10
    max_generations = 200
    i = 0
    j = 0
    z = 0
    for generation in range(max_generations):
        print "Generation: " + str(generation)
        print "Best Fitness: "
        best_fitness = min(fitness.iteritems(), key=operator.itemgetter(1))[1]
        print best_fitness
        if (float(best_fitness) <= 0.60 and i == 0):
            key = min(fitness.iteritems(), key=operator.itemgetter(1))[0]
            print key
            print population[int(key)]
            i = i + 1
        if (float(best_fitness) <= 0.50 and j == 0):
            key = min(fitness.iteritems(), key=operator.itemgetter(1))[0]
            print key
            print population[int(key)]
            j = j + 1
        if (float(best_fitness) <= 0.40 and z == 0):
            key = min(fitness.iteritems(), key=operator.itemgetter(1))[0]
            print key
            print population[int(key)]
            z = z + 1
        if (float(best_fitness) <= 0.30):
            key = min(fitness.iteritems(), key=operator.itemgetter(1))[0]
            print key
            print population[int(key)]
            break
        # print "Population: "
        # print population
        # Select Parents using Tournament Selection
        parent_1,parent_2 = Select_Parents(population,fitness,k)
        # print "Selected Parents: "
        # print population[parent_1]
        # print population[parent_2]
        # Procreate using BLX-0.5 Crossover
        pchild_1,pchild_2 = Procreate(population,parent_1,parent_2)
        # print "Children: "
        # print child_1
        # print child_2
        # Apply Gaussian Mutation with 0,1
        child_1, child_2 = Mutate(pchild_1,pchild_2,sigma)
        children = {}
        children[1] = child_1
        children[2] = child_2
        # Evaluate the fitness of children
        fitness_children = Evaluate(options.feature_files, children, sigma)
        # print "Fitness of Children: "
        # print fitness_children
        # Replace worst individuals in the population with the children (Steady State GA)
        worst_1, worst_2 = Select_Survivors(fitness)
        population[worst_1] = child_1
        population[worst_2] = child_2
        fitness[worst_1] = fitness_children[1]
        fitness[worst_2] = fitness_children[2]
        # print "Next Generation: "
        # print population
    key = min(fitness.iteritems(), key=operator.itemgetter(1))[0]
    print key
    print population[int(key)]

if __name__ == "__main__":
    main()