import math
from collections import Counter

#Euclidean Distance Squared
def euclidean_dist(t_q,t_i):
    sum = 0.0
    for i in range(0,len((t_q))):
        sum += math.pow((float(t_q[i])-float(t_i[i])),2.0)
    return math.sqrt(sum)

def getFS(train_set,test_set,sigma,desired_outputs):
    test_feature = test_set[0].split(',')
    hfs = []
    desired_outputs_list = []

    for feature in train_set:
        feature_temp = feature.split(',')
        author = feature_temp[0]
        desired_outputs_list.append(desired_outputs[author])
        dist_sqrd = 0.0
        for i in range(1, len((feature_temp))):
            dist_sqrd += math.pow((float(feature_temp[i]) - float(test_feature[i])), 2.0)
        hf = math.exp(-dist_sqrd/pow((2.0 * sigma),2.0))
        hfs.append(hf)

    return hfs,desired_outputs_list

def main(feature_files,sigma,desired_outputs_vector):
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
        c1 = Counter(features)
        c2 = Counter(test)
        diff = c1 - c2
        train = list(diff.elements())

        test_set.append(test[0].strip())
        true_label = test_set[0].split(',')[0]
        if true_label.isdigit():
            true_label = int(true_label)

        authors = []
        for feature in train:
            feature = feature.strip()
            train_set.append(feature)
            feature_list = feature.split(',')
            if feature_list[0] not in authors:
                authors.append(feature_list[0])

        # desired outputs
        desired_outputs = {}
        for feature in range(0, len(authors)):
            desired_output = [0] * len(authors)
            desired_output[feature] = desired_outputs_vector[feature]
            desired_outputs[authors[feature]] = desired_output

        # get fire strings
        hfs,desired_outputs_list = getFS(train_set,test_set,sigma,desired_outputs)

        S_1 = [0.0] * len(authors)
        S_2 = 0.0
        for j in range(0,len(hfs)):
            temp_list = [hfs[j]*d for d in desired_outputs_list[j]]
            S_1 = [x+y for x,y in zip(S_1,temp_list)]
            S_2 = S_2 + hfs[j]

        prediction_list = [s1/S_2 for s1 in S_1]
        prediction_index = prediction_list.index(max(prediction_list))
        prediction = authors[prediction_index]
        if prediction.isdigit():
            prediction = int(prediction)

        if (prediction == true_label):
            TP = TP + 1
        else:
            FP = FP + 1

    accuracy = float(TP)/float(TP + FP)
    return accuracy

if __name__ == "__main__":
    main()