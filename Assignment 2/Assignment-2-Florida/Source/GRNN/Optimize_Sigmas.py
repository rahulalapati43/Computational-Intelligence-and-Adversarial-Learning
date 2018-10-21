import numpy
import optparse
import itertools
import GRNN_Sigma

def main():
    # defining the way i want to capture user input
    parser = optparse.OptionParser()
    parser.add_option('--feature_files', dest='feature_files',
                      default='',  # default empty!
                      help='location of feature files')

    (options, args) = parser.parse_args()

    # assigning the user input
    feature_files = options.feature_files

    feature_files = open(feature_files,'r')
    features = feature_files.readlines()

    train_set = []
    for feature in features:
        feature = feature.strip()
        train_set.append(feature)

    distances = []
    for a, b in itertools.combinations(train_set, 2):
        a_feature = a.split(',')
        b_feature = b.split(',')
        distance = GRNN_Sigma.euclidean_dist(a_feature[1:], b_feature[1:])
        distances.append(distance)

    d_max = max(distances)
    # d_min = min(distances)
    #
    # if d_min <= 0.0:
    #     d_min = d_min + 0.1

    d_min = 0.05
    accuracy_list = []
    error_list = []
    for sigma in numpy.arange(d_min,d_max,0.005):
        accuracy = GRNN_Sigma.main(options.feature_files, sigma)
        accuracy_list.append(accuracy)
        error = 1 - accuracy
        error_list.append(error)

        print str(sigma) + " "  + str(accuracy) + " " + str(error)

if __name__ == "__main__":
    main()