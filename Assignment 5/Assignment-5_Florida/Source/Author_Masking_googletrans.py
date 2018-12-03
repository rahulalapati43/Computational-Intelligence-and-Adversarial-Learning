from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
import optparse
import re
from googletrans import Translator
from googletrans import LANGUAGES

def paraphraseable(tag):
     return tag.startswith('NN') or tag == 'VB' or tag.startswith('JJ')

def synonyms(word, tag):
     lemma_lists = [ss.lemmas() for ss in wn.synsets(word, pos(tag))]
     lemmas = [lemma.name() for lemma in sum(lemma_lists, [])]
     return set(lemmas)

def pos(tag):
    if tag.startswith('NN'):
        return wn.NOUN
    elif tag.startswith('V'):
        return wn.VERB

def tag(sentence):
    words = word_tokenize(sentence)
    words = pos_tag(words)
    return words

def synonymIfExists(sentence):
    for (word, t) in tag(sentence):
        if paraphraseable(t):
            syns = synonyms(word, t)
            if syns:
                if len(syns) > 1:
                    yield [word, list(syns)]
                    continue
        yield [word, []]

def getParaphrase(sentence):
        return [x for x in synonymIfExists(sentence)]

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
            line = re.sub(r'[^\x00-\x7F]+', '', line)
            # paraphrases = getParaphrase(line)
            #
            # str = ""
            # for paraphrase in paraphrases:
            #     if len(paraphrase[1]) > 0:
            #         str = str + paraphrase[1][0].encode('ascii', 'ignore')
            #         str = str + " "
            #     else:
            #         str = str + paraphrase[0]
            #         str = str + " "
            paraphrased_lines.append(line)

        LANGCODES = dict(map(reversed, LANGUAGES.items()))

        translator = Translator()
        trans_lines = paraphrased_lines
        for lang in LANGCODES.values():
            print lang
            trans_lines = translated_lines
            translated_lines = []
            for line in trans_lines:
                line = re.sub(r'[^\x00-\x7F]+', '', line)
                trans_line = translator.translate(line, dest='ja')
                translated_lines.append(trans_line.text)

        # ja_translated_lines = []
        # for line in paraphrased_lines:
        #     line = re.sub(r'[^\x00-\x7F]+', '', line)
        #     trans_line = translator.translate(line, dest='ja')
        #     ja_translated_lines.append(trans_line.text)
        #
        # ko_translated_lines = []
        # for line in paraphrased_lines:
        #     line = re.sub(r'[^\x00-\x7F]+', '', line)
        #     trans_line = translator.translate(line, dest='ko')
        #     ko_translated_lines.append(trans_line.text)
        #
        # en_translated_lines = []
        # for line in ko_translated_lines:
        #     trans_line = translator.translate(line)
        #     en_translated_lines.append(trans_line.text)

        output_file_name = writing_sample.split('.')
        output_file = open(output_file_name[0] + "_masked.txt",'w+')
        for line in translated_lines:
            output_file.write(line + "\n")

        output_file.close()
