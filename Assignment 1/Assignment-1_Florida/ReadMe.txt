------------------
Usage Instructions
------------------

To run the Feature_Extractor.py, please follow the instructions mentioned below:

1. For help:

   python Feature_Extractor.py -h

2. Sample command for execution:

   python Feature_Extractor.py --writing_samples=C:\Users\Buji\PycharmProjects\CI_Assignment_1\SEC_SportsWriters_Dataset --dataset_type=SEC-SportsWriters                  --feature_files=C:\Users\Buji\PycharmProjects\CI_Assignment_1\raw.txt --normalized_feature_files=C:\Users\Buji\PycharmProjects\CI_Assignment_1\normalized.txt
   
where 
		- writing_samples is the location of the directory consisting of the writing samples
                - dataset_type: pass "CASIS-25" if the writing samples belong to CASIS-25 dataset or "SEC-SportsWriters" if the writing samples belong to SEC Sports                                 Writers
                - feature_files is the location with the name of the file where you want to store the raw feature vectors 
		- normalized_feature_files is the location with the name of the file where you want to store the normalized feature vectors.

Note: Apart from the required directories and files, the "Miscellaneous" directory consists of the "Dataset_Statistics.py" program and also the statistics of CASIS-25       and SEC Sports Writers Datasets.