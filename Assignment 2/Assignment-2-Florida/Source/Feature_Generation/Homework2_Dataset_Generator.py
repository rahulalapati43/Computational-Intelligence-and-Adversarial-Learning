import Data_Utils
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.feature_extraction.text import TfidfTransformer
import optparse

parser = optparse.OptionParser()
parser.add_option('--raw_feature_file', dest='raw_feature_file',
                  default='',  # default empty!
                  help='location of raw feature file')

(options, args) = parser.parse_args()

# assigning the user input
raw_feature_file = options.raw_feature_file

oldCU_X, Y = Data_Utils.Get_Casis_CUDataset(raw_feature_file)

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

raw_feature_file = raw_feature_file.split('.')

file = open(raw_feature_file[0] + '_ncu.txt', 'w')
for i in range(0,len(oldCU_X)):
    file.write(str(Y[i]))
    for j in range(0,len(oldCU_X[i])):
        file.write("," + str(oldCU_X[i,j]))
    file.write("\n")
file.close()

file = open(raw_feature_file[0] + '_tsncu.txt', 'w')
for i in range(0,len(CU_X)):
    file.write(str(Y[i]))
    for j in range(0,len(CU_X[i])):
        file.write("," + str(CU_X[i,j]))
    file.write("\n")
file.close()

d = []
t = []

with open(raw_feature_file[0] + "_tsncu.txt", "r") as feature_file:
    for line in feature_file:
        line = line.strip().split(",")
        d.append(line[0])
        t.append([float(x) for x in line[1:]])


       
