import optparse
import pickle
import Data_Utils
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.feature_extraction.text import TfidfTransformer

def predict_author(model_file,raw_feature_file):
    CU_X, Y = Data_Utils.Get_Casis_CUDataset(raw_feature_file)

    scaler = StandardScaler()
    tfidf = TfidfTransformer(norm=None)
    dense = Data_Utils.DenseTransformer()

    # tf-idf
    tfidf.fit(CU_X)
    CU_train_data = dense.transform(tfidf.transform(CU_X))

    # standardization
    scaler.fit(CU_train_data)
    CU_train_data = scaler.transform(CU_train_data)

    # normalization
    CU_train_data = normalize(CU_train_data)

    model = pickle.load(open(model_file, 'rb'))
    print Y
    print model.predict(CU_train_data)

if __name__ == '__main__':
    # defining the way i want to capture user input
    parser = optparse.OptionParser()
    parser.add_option('--model_file', dest='model_file',
                      default='',  # default empty!
                      help='trained model file')
    parser.add_option('--raw_feature_file', dest='raw_feature_file',
                      default='',  # default empty!
                      help='raw feature file')

    (options, args) = parser.parse_args()

    # assigning the user input
    model_file = options.model_file
    raw_feature_file = options.raw_feature_file

    predict_author(model_file,raw_feature_file)
