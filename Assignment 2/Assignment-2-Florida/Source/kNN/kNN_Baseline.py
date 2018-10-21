import math
import optparse
import collections
import operator

#Euclidean Distance Squared
def euclidean_dist(t_q,t_i):
    sum = 0.0
    for i in range(0,len((t_q))):
        sum += math.pow((float(t_q[i])-float(t_i[i])),2.0)
    return math.sqrt(sum)

def getNeighbors(train_set,test_set,k):
    test_feature = test_set[0].split(',')
    distances = {}

    for feature in train_set:
        feature_temp = feature.split(',')
        distance = euclidean_dist(feature_temp[1:],test_feature[1:])
        distances[feature] = distance

    distances_sorted_by_value = collections.OrderedDict(sorted(distances.items(), key=lambda x: x[1]))

    neighbors = distances_sorted_by_value.items()
    return neighbors[:k]

def getLabel(neighbors):
    keys = []
    for neighbor in neighbors:
        label = neighbor[0].split(',')[0]
        if label.isdigit():
            label = int(label)
        keys.append(label)

    labels = dict.fromkeys(keys,0)
    for neighbor in neighbors:
        label = neighbor[0].split(',')[0]
        if label.isdigit():
            label = int(label)
        labels[label] = labels[label] + 1

    return max(labels.iteritems(), key=operator.itemgetter(1))[0]

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

        # get predictions
        prediction = getLabel(neighbors)
        if (prediction == true_label):
            TP = TP + 1
        else:
            FP = FP + 1

    accuracy = float(TP)/float(TP + FP)
    print str(TP) + " " + str(FP) + " " + str(accuracy) + "\n"

if __name__ == "__main__":
    main()