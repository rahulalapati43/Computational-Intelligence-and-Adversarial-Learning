import DriverCode
import Data_Utils
import optparse
import random
import os
import operator
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
    child = []
    for i in range(0,len(parent_1)):
        temp = []
        temp.append(parent_1[i])
        temp.append(parent_2[i])
        child_element = random.sample(temp,1)
        child.append(child_element[0])

    return child

def mutation(child):
    mutation_rate = 0.05
    mutate_child = []
    for i in range(0,len(child)):
        random_number = random.uniform(0,1)
        if random_number <= mutation_rate:
            mutate_child.append(child[i] + random.gauss(0,1))
        else:
            mutate_child.append(child[i])

    return mutate_child

def evaluateFitness(raw_feature_file,CU_X,Y,child,num):
    transformed_file_name = raw_feature_file.split('.')[0] + "_SSGA_Improvement_transformed_" + str(num) + ".txt"
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
            tCU_X.append(float(CU_X[feature][e]) * float(child[e]))

        string = ','.join(str(e) for e in tCU_X)
        string = str(Y[feature]) + ',' + string
        transformed_file.write(string + "\n")
    transformed_file.close()

    # evaluate fitness of the initial population
    fitness = DriverCode.classifier(transformed_file_name)
    os.remove(transformed_file_name)
    return fitness

def main(raw_feature_file):

    #initialize population of size 25
    population = initializePopulation()
    print "Initial Population:"
    print population

    #prepare the initial population for evaluating fitness
    fitness = {}
    CU_X, Y = Data_Utils.Get_Casis_CUDataset(raw_feature_file)
    for i in range(0,len(population)):
        fitness[i] = evaluateFitness(raw_feature_file,CU_X,Y,population[i],i)
    print "Fitness of Initial Population:"
    print fitness

    child_num = 0
    iterations = []
    best_individual_fitness = []
    while (child_num < 4975):
        #for plotting
        iterations.append(child_num)
        best_ind_fit = max(fitness.iteritems(), key=operator.itemgetter(1))[1]
        best_individual_fitness.append(best_ind_fit)

        #select parents using tournament selection
        parent_1, parent_2 = selectParents(population,fitness)
        print "parents:"
        print population[parent_1]
        print population[parent_2]

        #procreate children using uniform crossover
        child = procreate(population[parent_1],population[parent_2])
        print "child:"
        print child

        #mutate the child
        mutate_child = mutation(child)
        print "mutated child:"
        print mutate_child
        child_num = child_num + 1

        #evaluate fitness of the child
        child_fitness = evaluateFitness(raw_feature_file,CU_X,Y,mutate_child,child_num)
        print child_fitness

        #replace the worst individual in the population with the child
        worst_individual = min(fitness.iteritems(), key=operator.itemgetter(1))[0]
        population[worst_individual] = mutate_child
        fitness[worst_individual] = child_fitness
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

    output_file_name = "C:\Users\Buji\PycharmProjects\CI_Assignment_3\CASIS-25_Features\Steady_State_GA_Improvement_output.txt"
    output_file = open(output_file_name,'w+')

    best_fitness = 0.0
    max_performances = []

    #run GEFes 10 times
    for run in range(1,11):
        output_file.write("run:" + str(run) + "\n")
        population,fitness,iterations,best_individual_fitness = main(raw_feature_file)

        plt.figure()
        plt.plot(iterations,best_individual_fitness)
        plt.title("Best Individual per Generation")
        plt.xlabel("Iterations")
        plt.ylabel("Accuracy")
        plot_name = "C:\Users\Buji\PycharmProjects\CI_Assignment_3\Plots" + "\SSGA_Improvement_" + str(run) + ".png"
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
    average_fitness = float(sum(max_performances)/len(max_performances))
    output_file.write("Average Fitness:" + str(average_fitness) + "\n")
    output_file.write("Best Fitness:" + str(best_fitness) + "\n")
    output_file.close()