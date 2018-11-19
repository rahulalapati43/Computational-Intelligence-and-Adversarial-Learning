import Data_Utils
from sklearn import svm
import pickle
import optparse
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.feature_extraction.text import TfidfTransformer

def classifier(raw_feature_vectors,feature_mask):
    CU_X, Y = Data_Utils.Get_Casis_CUDataset(raw_feature_vectors)

    scaler = StandardScaler()
    tfidf = TfidfTransformer(norm=None)
    dense = Data_Utils.DenseTransformer()

    # tf-idf
    tfidf.fit(CU_X)
    CU_train_data = dense.transform(tfidf.transform(CU_X))

    print "after tfidf"
    print CU_train_data

    min_value = 0.0
    max_value = 0.0
    for fv in CU_train_data:
        list_min = min(fv)
        list_max = max(fv)

        if (min_value > list_min):
            min_value = list_min

        if (max_value < list_max):
            max_value = list_max

    print min_value
    print max_value

    # standardization
    scaler.fit(CU_train_data)
    CU_train_data = scaler.transform(CU_train_data)

    print "after std"
    print CU_train_data

    min_value = 0.0
    max_value = 0.0
    for fv in CU_train_data:
        list_min = min(fv)
        list_max = max(fv)

        if (min_value > list_min):
            min_value = list_min

        if (max_value < list_max):
            max_value = list_max

    print min_value
    print max_value

    # normalization
    CU_train_data = normalize(CU_train_data)

    print "after norm"
    print CU_train_data

    min_value = 0.0
    max_value = 0.0
    for fv in CU_train_data:
        list_min = min(fv)
        list_max = max(fv)

        if (min_value > list_min):
            min_value = list_min

        if (max_value < list_max):
            max_value = list_max

    print min_value
    print max_value

    # applying best feature mask
    tCU_train_data = []
    for fv in CU_train_data:
        tCU_X = []
        for i in range(0,len(fv)):
            tCU_X.append(fv[i] * feature_mask[i])
        tCU_train_data.append(tCU_X)

    print "after applying feature mask"
    print tCU_train_data

    # finding the min and max for EC Initial Population Range
    min_value = 0.0
    max_value = 0.0
    for fv in tCU_train_data:
        list_min = min(fv)
        list_max = max(fv)

        if (min_value > list_min):
            min_value = list_min

        if (max_value < list_max):
            max_value = list_max

    print min_value
    print max_value

    lsvm = svm.LinearSVC()

    train_labels = Y
    train_data = tCU_train_data

    # evaluation
    lsvm.fit(train_data, train_labels)
    pickle.dump(lsvm,open('C:\Users\Buji\PycharmProjects\CI_Assignment_4\Models\EEDA_SEC.pickle','wb'))

if __name__ == '__main__':
    # defining the way i want to capture user input
    parser = optparse.OptionParser()
    parser.add_option('--raw_feature_file', dest='raw_feature_file',
                      default='',  # default empty!
                      help='raw feature vector file')

    (options, args) = parser.parse_args()

    # assigning the user input
    raw_feature_file = options.raw_feature_file

    feature_mask = [-0.2090607938301814, 6.342518636940124, 1.8391213765435321, -1.7070520871193402, 0.5104609576084846, 2.3263153810478343, 0.8243267863200422, 5.70909264974985, 2.669426818607152, -1.7103638738210152, 4.335652986845748, 0.7263612276387074, 0.5838294726289446, 4.295144539466348, -1.775321748421637, -3.676128860860588, 1.2892233102646957, -0.04840481930127655, -4.502591235977459, 0.209388111812418, 1.8403750675012476, -0.3000553713807291, -1.329709355437878, -2.4393719573900743, 2.5993389911097387, -1.7461701522482131, 1.591527512352207, -0.6894978602649195, -2.734938735461069, 0.49774190180500155, 2.5990582530031925, 4.897915147310222, -0.6966279109656763, 0.06626638321230516, -0.7237570124229586, 3.8666300681351755, 3.0549077194195933, 0.7675689634634384, 1.8573469642329175, -0.053724600925039015, 0.896732682994167, -0.9689600892163384, 0.20238843348836788, 1.618966125197305, 0.3660112734148079, -0.49734814320604515, 0.7919695264399397, 0.2935019637725889, 6.128643573836772, -0.5248231383821871, -0.16272248882980167, -1.5536057960772158, 1.4954902729198318, 1.349716667639277, 2.177161072545596, 1.3429866846935483, -3.4532409474282777, 0.3149516976878108, -0.19480526266387546, 1.9769483781696104, -1.763363452293361, 0.8353930713326062, 0.8986335741413036, 1.4541222042603197, -0.738552015737199, 0.9900745045792186, -1.2926361763248062, -2.151518268253445, 3.396677314326144, -0.2835430500478062, -0.9324324122896848, 0.22879855188860165, -3.1470991787374047, -0.3110575418462209, 1.6689244619522217, -0.6073836452547197, 4.153983495511225, -0.7177135460639879, -1.5239563235271403, 0.6768680135384592, -0.1799155021326011, -2.185785444067404, -3.0845809639142177, 1.1280356503327145, 2.3346168910684755, 1.090283388505882, 2.8202836818251833, -2.4384373356814293, 0.9935085582966705, 0.25304556672090706, -1.7840460539195278, -2.1542148670623513, -0.3808599249955234, 3.054803401402629, -3.2403707058637563]
    classifier(raw_feature_file,feature_mask)
