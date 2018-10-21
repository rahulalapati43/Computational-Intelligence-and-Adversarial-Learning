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


oldCU_X, Y = Data_Utils.Get_Casis_CUDataset()

scaler = StandardScaler()
tfidf = TfidfTransformer(norm=None)
dense = Data_Utils.DenseTransformer()

CU_X = oldCU_X

tfidf.fit(CU_X)
CU_X = dense.transform(tfidf.transform(CU_X))

scaler.fit(CU_X)
CU_X = scaler.transform(CU_X)

CU_X = normalize(CU_X)

oldCU_X = normalize(oldCU_X)

file = open('Homework2_Dataset1_ncu.txt', 'w')
for i in range(0,len(oldCU_X)):
    file.write(str(Y[i]))
    for j in range(0,len(oldCU_X[i])):
        file.write("," + str(oldCU_X[i,j]))
    file.write("\n")
file.close()

file = open('Homework2_Dataset1_tsncu.txt', 'w')
for i in range(0,len(CU_X)):
    file.write(str(Y[i]))
    for j in range(0,len(CU_X[i])):
        file.write("," + str(CU_X[i,j]))
    file.write("\n")
file.close()

d = []
t = []

with open("Homework2_Dataset1_tsncu.txt", "r") as feature_file:
    for line in feature_file:
        line = line.strip().split(",")
        d.append(line[0])
        t.append([float(x) for x in line[1:]])


       
