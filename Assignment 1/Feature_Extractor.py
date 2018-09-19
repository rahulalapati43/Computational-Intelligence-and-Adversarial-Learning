import os
import optparse
import math
from collections import OrderedDict

#defining the way i want to capture user input
parser = optparse.OptionParser()
parser.add_option('--writing_samples',dest='writing_samples',
                  default='',#default empty!
                  help='location of writing samples')
parser.add_option('--dataset_type',dest='dataset_type',
                  default='',#default empty!
                  help='CASIS-25 or SEC-SportsWriters')
parser.add_option('--feature_files',dest='feature_files',
                  default='',#default empty!
                  help='location to store raw feature file')
parser.add_option('--normalized_feature_files',dest='normalized_feature_files',
                  default='',#default empty!
                  help='location to store normalized feature file')

(options,args) = parser.parse_args()

#assigning the user input
writing_samples = options.writing_samples
dataset_type = options.dataset_type
feature_files = options.feature_files
normalized_feature_files = options.normalized_feature_files

#files (writing samples) inside the directory
writing_samples_files = os.listdir(writing_samples)

#ASCII order 32 to 126 : count 95
keys = []
for x in range(32,127):
    keys.append(chr(x))

#output files for term frequencies and normalized feature vectors
raw_fv_file = open(feature_files,'w+')
normalized_fv_file = open(normalized_feature_files, 'w+')

for file in writing_samples_files:
    #initializing a dictionary with keys as ASCII order 32 to 126 and their values as 0.0
    raw_fv_dict = OrderedDict.fromkeys(keys,0.0)
    writing_sample = open(writing_samples + "/" + file,'r')
    #getting the character count
    for line in writing_sample:
        for char in line:
            if char in keys:
                raw_fv_dict[char] += 1

    #getting the file name to append it to the begining of the line
    if (dataset_type == "CASIS-25"):
        file = file.split('_')
        raw_fv_file.write(file[0] + ',')
        normalized_fv_file.write(file[0] + ',')
    elif (dataset_type == "SEC-SportsWriters"):
        file = file.split('_')
        raw_fv_file.write(file[0] + '_' + file[1] + ',')
        normalized_fv_file.write(file[0] + '_' + file[1] + ',')

    #getting the term frequencies per file
    values = raw_fv_dict.values()

    #calculating magnititude
    squared_sum = 0
    for value in values:
        squared_sum += math.pow((value - 0), 2)

    magnititude = math.sqrt(squared_sum)

    #getting the normalized feature vectors
    for value in range(0,len(values)-1):
        raw_fv_file.write(str(values[value]) + ',')
        normalized_fv_file.write(str(values[value]/magnititude) + ',')

    raw_fv_file.write(str(values[len(values)-1]) + '\n')
    normalized_fv_file.write(str(values[len(values)-1]/magnititude) + '\n')

raw_fv_file.close()
normalized_fv_file.close()