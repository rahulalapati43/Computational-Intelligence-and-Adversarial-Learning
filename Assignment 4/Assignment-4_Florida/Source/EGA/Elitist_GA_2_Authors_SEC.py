import optparse
import random
import operator
from collections import Counter
import matplotlib.pyplot as plt
import pickle

def initializePopulation():
    population_size = 25
    population = {}
    for i in range(0,population_size):
        individual = []
        for j in range(0,95):
            individual.append(random.uniform(-0.297557693329,0.660505575927))
        population[i] = individual

    return population

def evaluateFitness(model_file,child):

    desired_decision_function = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

    # evaluate fitness of the initial population
    eval_data = []
    eval_data.append(child)
    model = pickle.load(open(model_file, 'rb'))
    decision_function = model.decision_function(eval_data)[0]
    print "decision function:"
    print decision_function
    df_file.write("".join(str(decision_function)))
    squared_difference = 0.0
    for i in range(0, len(decision_function)):
        squared_difference = squared_difference + ((decision_function[i] - desired_decision_function[i]) * (decision_function[i] - desired_decision_function[i]))

    fitness = squared_difference
    df_file.write(str(fitness) + "\n")
    return fitness

def selectParents(population,fitness):
    parents = random.sample(population,2)
    temp_fitness = {}
    temp_fitness[parents[0]] = fitness[parents[0]]
    temp_fitness[parents[1]] = fitness[parents[1]]
    parent_1 = min(temp_fitness.iteritems(), key=operator.itemgetter(1))[0]

    parents = random.sample(population, 2)
    temp_fitness = {}
    temp_fitness[parents[0]] = fitness[parents[0]]
    temp_fitness[parents[1]] = fitness[parents[1]]
    parent_2 = min(temp_fitness.iteritems(), key=operator.itemgetter(1))[0]

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

def main(model_file):

    # initialize population of size 25
    population = initializePopulation()
    print "Initial Population:"
    print population

    # prepare the initial population for evaluating fitness
    iterations = []
    squared_difference_fitness = []
    best_individual_fitness = []
    fitness = {}
    eval_no = 0
    for i in range(0, len(population)):
        fitness[i] = evaluateFitness(model_file, population[i])
        iterations.append(eval_no)
        squared_difference_fitness.append(fitness[i])
        best_ind_fit = min(fitness.iteritems(), key=operator.itemgetter(1))[1]
        best_individual_fitness.append(best_ind_fit)
        eval_no = eval_no + 1

    print "Fitness of Initial Population:"
    print fitness

    child_num = 0
    while (child_num < int(4975/24)):

        #create 24 offsprings, two offsprings at a time using uniform crossover
        children = {}
        children_fitness = {}
        num = 0
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
            child_fitness_1 = evaluateFitness(model_file, mutate_child_1)
            print child_fitness_1

            # for plotting
            iterations.append(eval_no)
            squared_difference_fitness.append(child_fitness_1)
            best_ind_fit = min(fitness.iteritems(), key=operator.itemgetter(1))[1]
            best_individual_fitness.append(best_ind_fit)
            eval_no = eval_no + 1

            # evaluate fitness of the child
            child_fitness_2 = evaluateFitness(model_file, mutate_child_2)
            print child_fitness_2

            # for plotting
            iterations.append(eval_no)
            squared_difference_fitness.append(child_fitness_2)
            best_ind_fit = min(fitness.iteritems(), key=operator.itemgetter(1))[1]
            best_individual_fitness.append(best_ind_fit)
            eval_no = eval_no + 1

            children[num] = mutate_child_1
            children_fitness[num] = child_fitness_1
            num = num + 1
            children[num] = mutate_child_2
            children_fitness[num] = child_fitness_2
            num = num + 1

        child_num = child_num + 1

        # replace the worst 24 individuals in the population with the child
        num = 0
        best_individual = min(fitness.iteritems(), key=operator.itemgetter(1))[0]
        for i in range(0,len(population)):
            if (i != best_individual):
                population[i] = children[num]
                fitness[i] = children_fitness[num]
                num = num + 1

        print "Population after generation of child:" + str(child_num)
        print population
        print "Fitness:"
        print fitness

    return population,fitness,iterations,squared_difference_fitness,best_individual_fitness

if __name__ == '__main__':
    # defining the way i want to capture user input
    parser = optparse.OptionParser()
    parser.add_option('--model_file', dest='model_file',
                      default='',  # default empty!
                      help='trained model file')

    (options, args) = parser.parse_args()

    # assigning the user input
    model_file = options.model_file

    output_file_name = "C:\Users\Buji\PycharmProjects\CI_Assignment_4\SEC_SportsWriters_Features\Elitist_GA_2_Authors_output.txt"
    output_file = open(output_file_name, 'w+')

    df_file_name = "C:\Users\Buji\PycharmProjects\CI_Assignment_4\SEC_SportsWriters_Features\Elitist_GA_2_Authors_df.txt"
    df_file = open(df_file_name, 'w+')

    best_fitness = 9999999999999999
    max_performances = []

    # run GEFes 10 times
    for run in range(1, 11):
        output_file.write("run:" + str(run) + "\n")
        population, fitness, iterations, squared_difference_fitness, best_individual_fitness = main(model_file)
        print len(iterations)
        print len(squared_difference_fitness)
        print len(best_individual_fitness)

        plt.figure()
        plt.scatter(iterations,squared_difference_fitness,s=2)
        plt.scatter(iterations,best_individual_fitness,s=2,edgecolors='red')
        plt.title("Online Plot for Two Authors")
        plt.xlabel("Evaluations")
        plt.ylabel("Squared Difference")
        plot_name = "C:\Users\Buji\PycharmProjects\CI_Assignment_4\Plots" + "\EGA_2_Authors_SEC_" + str(run) + ".png"
        plt.savefig(plot_name)

        max_fitness = min(fitness.iteritems(), key=operator.itemgetter(1))[1]
        max_performances.append(max_fitness)

        if (best_fitness > max_fitness):
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
    df_file.close()