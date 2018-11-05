import Data_Utils
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler, normalize
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import StratifiedKFold
from sklearn import preprocessing
import numpy as np
from sklearn.model_selection import cross_val_score

def classifier(raw_feature_vectors):
    CU_X, Y = Data_Utils.Get_Casis_CUDataset(raw_feature_vectors)

    #rbfsvm = svm.SVC()
    lsvm = svm.LinearSVC()
    #mlp = MLPClassifier(max_iter=2000)

    skf = StratifiedKFold(n_splits=6, shuffle=True, random_state=0)
    fold_accuracy = []

    # scaler = StandardScaler()
    # tfidf = TfidfTransformer(norm=None)
    # dense = Data_Utils.DenseTransformer()

    for train, test in skf.split(CU_X, Y):
        #train split
        CU_train_data = CU_X[train]
        train_labels = Y[train]

        #test split
        CU_eval_data = CU_X[test]
        eval_labels = Y[test]

        # # tf-idf
        # tfidf.fit(CU_train_data)
        # CU_train_data = dense.transform(tfidf.transform(CU_train_data))
        # CU_eval_data = dense.transform(tfidf.transform(CU_eval_data))
        #
        # # standardization
        # scaler.fit(CU_train_data)
        # CU_train_data = scaler.transform(CU_train_data)
        # CU_eval_data = scaler.transform(CU_eval_data)
        #
        # # normalization
        # CU_train_data = normalize(CU_train_data)
        # CU_eval_data = normalize(CU_eval_data)

        train_data =  CU_train_data
        eval_data = CU_eval_data

        # evaluation
        #rbfsvm.fit(train_data, train_labels)
        lsvm.fit(train_data, train_labels)
        #mlp.fit(train_data, train_labels)

        # decision function
        # print "Decision Function:"
        # print lsvm.decision_function(train_data)
        # print lsvm.decision_function(eval_data)

        #rbfsvm_acc = rbfsvm.score(eval_data, eval_labels)
        lsvm_acc = lsvm.score(eval_data, eval_labels)
        #mlp_acc = mlp.score(eval_data, eval_labels)
        #fold_accuracy.append((lsvm_acc, rbfsvm_acc, mlp_acc))
        fold_accuracy.append(lsvm_acc)

    #print(np.mean(fold_accuracy, axis = 0))
    #mean = np.mean(fold_accuracy, axis = 0)
    mean = float(sum(fold_accuracy)/len(fold_accuracy))
    #print mean
    return mean
