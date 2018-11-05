import DriverCode
import Data_Utils
import optparse
import random
import os
import operator
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.feature_extraction.text import TfidfTransformer

def initializePopulation():
    population_size = 25
    population = {}
    for i in range(0,population_size):
        individual = []
        for j in range(0,95):
            individual.append(random.uniform(0,1))
        population[i] = individual

    return population

def evaluateFitness(raw_feature_file,CU_X,Y,child,num):
    transformed_file_name = raw_feature_file.split('.')[0] + "_EGA_Improvement_transformed_" + str(num) +".txt"
    transformed_file = open(transformed_file_name, 'w+')

    scaler = StandardScaler()
    tfidf = TfidfTransformer(norm=None)
    dense = Data_Utils.DenseTransformer()

    # tf-idf
    tfidf.fit(CU_X)
    CU_X = dense.transform(tfidf.transform(CU_X))

    # standardization
    scaler.fit(CU_X)
    CU_X = scaler.transform(CU_X)

    # normalization
    CU_X = normalize(CU_X)

    for feature in range(0, len(CU_X)):
        tCU_X = []
        for e in range(0, len(CU_X[feature])):
            tCU_X.append(CU_X[feature][e] * child[e])

        string = ','.join(str(e) for e in tCU_X)
        string = str(Y[feature]) + ',' + string
        transformed_file.write(string + "\n")
    transformed_file.close()

    # evaluate fitness of the initial population
    fitness = DriverCode.classifier(transformed_file_name)
    os.remove(transformed_file_name)
    return fitness

def selectParents(population,fitness):
    parents = random.sample(population,2)
    temp_fitness = {}
    temp_fitness[parents[0]] = fitness[parents[0]]
    temp_fitness[parents[1]] = fitness[parents[1]]
    parent_1 = max(temp_fitness.iteritems(), key=operator.itemgetter(1))[0]

    parents = random.sample(population, 2)
    temp_fitness = {}
    temp_fitness[parents[0]] = fitness[parents[0]]
    temp_fitness[parents[1]] = fitness[parents[1]]
    parent_2 = max(temp_fitness.iteritems(), key=operator.itemgetter(1))[0]

    return parent_1, parent_2

def procreate(parent_1,parent_2):
    child_1 = []
    child_2 = []
    for i in range(0,len(parent_1)):
        temp = []
        temp.append(parent_1[i])
        temp.append(parent_2[i])
        child_element_1 = random.sample(temp,1)
        c1 = Counter(temp)
        c2 = Counter(child_element_1)
        diff = c1-c2
        child_element_2 = list(diff.elements())
        child_1.append(child_element_1[0])
        child_2.append(child_element_2[0])

    return child_1, child_2

def mutation(child_1,child_2):
    mutation_rate = 0.05
    mutate_child_1 = []
    mutate_child_2 = []
    for i in range(0,len(child_1)):
        random_number = random.uniform(0,1)
        if random_number <= mutation_rate:
            mutate_child_1.append(child_1[i] + random.gauss(0,1))
        else:
            mutate_child_1.append(child_1[i])

    for i in range(0,len(child_2)):
        random_number = random.uniform(0,1)
        if random_number <= mutation_rate:
            mutate_child_2.append(child_2[i] + random.gauss(0,1))
        else:
            mutate_child_2.append(child_2[i])

    return mutate_child_1, mutate_child_2

def main(raw_feature_file):

    # initialize population of size 25
    population = initializePopulation()
    print "Initial Population:"
    print population

    # prepare the initial population for evaluating fitness
    fitness = {}
    CU_X, Y = Data_Utils.Get_Casis_CUDataset(raw_feature_file)
    for i in range(0, len(population)):
        fitness[i] = evaluateFitness(raw_feature_file, CU_X, Y, population[i],i)
    print "Fitness of Initial Population:"
    print fitness

    child_num = 0
    iterations = []
    best_individual_fitness = []
    while (child_num < int(4975/24)):
        #for plotting
        iterations.append(child_num)
        best_ind_fit = max(fitness.iteritems(), key=operator.itemgetter(1))[1]
        best_individual_fitness.append(best_ind_fit)

        #create 24 offsprings, two offsprings at a time using uniform crossover
        children = {}
        children_fitness = {}
        num = 0
        temp = 0
        for i in range(0,12):
            # select parents using tournament selection
            parent_1, parent_2 = selectParents(population, fitness)
            print "parents:"
            print population[parent_1]
            print population[parent_2]

            # procreate children using uniform crossover
            child_1,child_2 = procreate(population[parent_1], population[parent_2])
            print "children:"
            print child_1
            print child_2

            # mutate the child
            mutate_child_1, mutate_child_2 = mutation(child_1,child_2)
            print "mutated child:"
            print mutate_child_1
            print mutate_child_2

            # evaluate fitness of the child
            child_fitness_1 = evaluateFitness(raw_feature_file, CU_X, Y, mutate_child_1, temp)
            print child_fitness_1
            temp = temp + 1

            # evaluate fitness of the child
            child_fitness_2 = evaluateFitness(raw_feature_file, CU_X, Y, mutate_child_2, temp)
            print child_fitness_2
            temp = temp + 1

            children[num] = mutate_child_1
            children_fitness[num] = child_fitness_1
            num = num + 1
            children[num] = mutate_child_2
            children_fitness[num] = child_fitness_2
            num = num + 1

        child_num = child_num + 1

        # replace the worst 24 individuals in the population with the child
        num = 0
        best_individual = max(fitness.iteritems(), key=operator.itemgetter(1))[0]
        for i in range(0,len(population)):
            if (i != best_individual):
                population[i] = children[num]
                fitness[i] = children_fitness[num]
                num = num + 1

        print "Population after generation of child:" + str(child_num)
        print population
        print "Fitness:"
        print fitness

    return population,fitness,iterations,best_individual_fitness

if __name__ == '__main__':
    # defining the way i want to capture user input
    parser = optparse.OptionParser()
    parser.add_option('--raw_feature_file', dest='raw_feature_file',
                      default='',  # default empty!
                      help='raw feature vector file')

    (options, args) = parser.parse_args()

    # assigning the user input
    raw_feature_file = options.raw_feature_file

    output_file_name = "C:\Users\Buji\PycharmProjects\CI_Assignment_3\CASIS-25_Features\Elitist_GA_Improvement_output.txt"
    output_file = open(output_file_name, 'w+')

    best_fitness = 0.0
    max_performances = []

    # run GEFes 10 times
    for run in range(1, 11):
        output_file.write("run:" + str(run) + "\n")
        population, fitness, iterations, best_individual_fitness = main(raw_feature_file)

        plt.figure()
        plt.plot(iterations,best_individual_fitness)
        plt.title("Best Individual per Generation")
        plt.xlabel("Iterations")
        plt.ylabel("Accuracy")
        plot_name = "C:\Users\Buji\PycharmProjects\CI_Assignment_3\Plots" + "\EGA_Improvement_" + str(run) + ".png"
        plt.savefig(plot_name)

        max_fitness = max(fitness.iteritems(), key=operator.itemgetter(1))[1]
        max_performances.append(max_fitness)

        if (best_fitness < max_fitness):
            best_fitness = max_fitness

        output_file.write("population:" + "\n")
        for key in population.keys():
            output_file.write(str(population[key]) + ' ' + str(fitness[key]))
            output_file.write("\n")

        output_file.write("Best Fitness:" + str(best_fitness) + "\n")

    output_file.write("Final:" + "\n")
    average_fitness = float(sum(max_performances) / len(max_performances))
    output_file.write("Average Fitness:" + str(average_fitness) + "\n")
    output_file.write("Best Fitness:" + str(best_fitness) + "\n")
    output_file.close()