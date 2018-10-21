import numpy
import optparse
import kNN_Distance_Weighted

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

    accuracy_list = []
    error_list = []
    for b in numpy.arange(0.5,6,0.5):
        accuracy = kNN_Distance_Weighted.main(options.feature_files, k, b)
        accuracy_list.append(accuracy)
        error = 1 - accuracy
        error_list.append(error)

        print str(b) + " "  + str(accuracy) + " " + str(error)

if __name__ == "__main__":
    main()