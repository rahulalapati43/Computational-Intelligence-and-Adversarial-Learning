import os
import optparse

parser = optparse.OptionParser()
parser.add_option('--dataset',dest='dataset',
                  default='',#default empty!
                  help='location of the dataset')
parser.add_option('--output_file',dest='output_file',
                  default='',#default empty!
                  help='location of the output file')

(options,args) = parser.parse_args()

dataset = options.dataset
output_file = options.output_file

out_file = open(output_file, 'w+')

dataset_files = os.listdir(dataset)
dataset_len = len(dataset_files)

char_total = 0
words_total = 0
lines_total = 0

for file in dataset_files:
    char_count = 0
    words_count = 0
    lines_count = 0
    data_file = open(dataset + "/" + file,'r')
    for line in data_file:
        lines_count = lines_count + 1
        words = line.split()
        words_count = words_count + len(words)
        for word in words:
            char_count = char_count + len(word)

    out_file.write("File Name: " + file + "\n")
    out_file.write("Char Count: " + str(char_count) + "\n")
    out_file.write("Word Count: " + str(words_count) + "\n")
    out_file.write("Lines Count: " + str(lines_count) + "\n")

    char_total = char_total + char_count
    words_total = words_total + words_count
    lines_total = lines_total + lines_count

out_file.write("Total Char Count: " + str(char_total) + "\n")
out_file.write("Total Word Count: " + str(words_total) + "\n")
out_file.write("Total Line Count: " + str(lines_total) + "\n")

char_avg = (char_total/dataset_len)
words_avg = (words_total/dataset_len)
lines_avg = (lines_total/dataset_len)

out_file.write("Average Char Count: " + str(char_avg) + "\n")
out_file.write("Average Word Count: " + str(words_avg) + "\n")
out_file.write("Average Line Count: " + str(lines_avg) + "\n")
out_file.close()


