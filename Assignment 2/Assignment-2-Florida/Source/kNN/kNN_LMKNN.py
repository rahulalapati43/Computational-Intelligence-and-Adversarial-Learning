import math
import optparse
import collections
import operator
import ast

#Euclidean Distance Squared
def euclidean_dist(t_q,t_i):
    sum = 0.0
    for i in range(0,len((t_q))):
        sum += math.pow((float(t_q[i])-float(t_i[i])),2.0)
    return math.sqrt(sum)

def getDistancesbyClass(train_set,test_set):
    test_feature = test_set[0].split(',')
    distances = {}
    for feature in train_set:
        distance = euclidean_dist(feature,test_feature[1:])
        distances[str(feature)] = distance

    return distances

def getNeighbors(train_set,test_set,k):
    features = {}

    for feature in train_set:
        feature_temp = feature.split(',')
        if feature_temp[0] in features:
            features[feature_temp[0]].append(feature_temp[1:])
        else:
            features[feature_temp[0]] = []
            features[feature_temp[0]].append(feature_temp[1:])

    neighbors_dict = {}
    for key in features.keys():
        distances = getDistancesbyClass(features[key],test_set)
        distances_sorted_by_value = collections.OrderedDict(sorted(distances.items(), key=lambda x: x[1]))
        neighbors = distances_sorted_by_value.items()
        neighbors_temp = neighbors[:k]
        neighbors_list = []
        for neighbor in neighbors_temp:
            neighbors_list.append(ast.literal_eval(neighbor[0]))
        neighbors_dict[key] = neighbors_list

    return neighbors_dict

def getLMs(neighbors):
    lms = {}
    for key in neighbors:
        mean_vector = []
        for col in zip(*neighbors[key]):
            col = map(float, col)
            mean_vector.append(float(sum(col))/len(col))
        lms[key] = mean_vector

    return lms

def getLabel(lmvs,test_set):
    test_feature = test_set[0].split(',')
    distances = {}
    for key in lmvs:
        distance = euclidean_dist(test_feature[1:],lmvs[key])
        distances[key] = distance

    return min(distances.iteritems(), key=operator.itemgetter(1))[0]

def main():
    # defining the way i want to capture user input
    parser = optparse.OptionParser()
    parser.add_option('--feature_files', dest='feature_files',
                      default='',  # default empty!
                      help='location of feature files')
    parser.add_option('--k', dest='k',
                      default='',  # default empty!
                      help='k value')

    (options, args) = parser.parse_args()

    # assigning the user input
    feature_files = options.feature_files
    k = int(options.k)

    feature_files = open(feature_files,'r')
    features = feature_files.readlines()

    TP = 0
    FP = 0
    # leave one out cross validation
    for i in range(0,len(features)):
        # load train and test datasets
        test_set = []
        train_set = []
        test = []
        test.append(features[i])
        c1 = collections.Counter(features)
        c2 = collections.Counter(test)
        diff = c1 - c2
        train = list(diff.elements())

        test_set.append(test[0].strip())
        true_label = test_set[0].split(',')[0]
        if true_label.isdigit():
            true_label = int(true_label)

        for feature in train:
            feature = feature.strip()
            train_set.append(feature)

        # get neighbors
        neighbors = getNeighbors(train_set,test_set,k)

        # get local mean vectors
        lmvs = getLMs(neighbors)

        # get predictions
        prediction = getLabel(lmvs,test_set)
        if prediction.isdigit():
            prediction = int(prediction)
        if (prediction == true_label):
            TP = TP + 1
        else:
            FP = FP + 1

    accuracy = float(TP)/float(TP + FP)
    print str(TP) + " " + str(FP) + " " + str(accuracy) + "\n"

if __name__ == "__main__":
    main()