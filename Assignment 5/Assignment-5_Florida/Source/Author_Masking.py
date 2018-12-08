import optparse
import re
from yandex_translate import YandexTranslate

if __name__ == '__main__':
        # defining the way i want to capture user input
        parser = optparse.OptionParser()
        parser.add_option('--writing_sample', dest='writing_sample',
                          default='',  # default empty!
                          help='location of writing sample')

        (options, args) = parser.parse_args()

        # assigning the user input
        writing_sample = options.writing_sample

        writing_sample_file = open(writing_sample,'r')
        writing_sample_file_list = writing_sample_file.readlines()

        paraphrased_lines = []
        for line in writing_sample_file_list:
            line = line.strip()
            paraphrased_lines.append(line)

        translator = YandexTranslate('trnsl.1.1.20181203T031441Z.73e6c071d315de8c.d99fa4b7549b8e4924af75707da5190b9deb115e')
        ru_translated_lines = []
        for line in paraphrased_lines:
            line = re.sub(r'[^\x00-\x7F]+', '', line)
            trans_line = translator.translate(line,'en-ru')
            ru_translated_lines.append(trans_line['text'][0])

        en_translated_lines = []
        for line in ru_translated_lines:
            trans_line = translator.translate(line,'ru-en')
            en_translated_lines.append(trans_line['text'][0])

        ar_translated_lines = []
        for line in en_translated_lines:
            trans_line = translator.translate(line, 'en-ar')
            ar_translated_lines.append(trans_line['text'][0])

        en_translated_lines = []
        for line in ar_translated_lines:
            trans_line = translator.translate(line, 'ar-en')
            en_translated_lines.append(trans_line['text'][0])

        output_file_name = writing_sample.split('.')
        output_file = open(output_file_name[0] + "_5.txt",'w+')
        for line in en_translated_lines:
            print line
            output_file.write(line + "\n")

        output_file.close()