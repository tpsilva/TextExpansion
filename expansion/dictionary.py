import subprocess
import os

import lingotranslator.translator as lingo_translator

STOPWORDS_PATH = "../res/stopwords.txt"

BABELNET_SHELL = "bash"
BABELNET_SCRIPT = "/opt/babelnet-api-1.0.1/run-babelnet.sh"
BABELNET_CONCEPTS_OPTION = "-TOKENTRANSLATION"
BABELNET_DIVIDER = "===DIVIDER==="


class EnglishDictionary:
    def __init__(self):
        f = open("../res/freeling.src", "r")
        self.words = [l.split()[0].lower() for l in f.readlines()]
        f.close()

    def exists(self, word):
        return word.lower() in self.words

class GenericDictionary:
    def __init__(self, filename):
        f = open(filename, "r")
        self.dictionary = dict(l.strip("\n").split("\t") for l in f.readlines())
        f.close()

    def translate(self, word):
        try:
            return self.dictionary[word.lower()]
        except:
            return word

class LingoDictionary:
    def __init__(self):
        self.mode = "YYN"
        lingo_translator.init(self.mode)

    def translate(self, line):
        return lingo_translator.translate(line)

class ConceptsDictionary:
    def __init__(self):
        self.lingo = LingoDictionary()
        self.cache = {}

        self.load_stopwords()

    def load_stopwords(self):
        module_path = os.path.dirname(__file__)
        stopwords_real_path = os.path.join(module_path, STOPWORDS_PATH)

        f = open(stopwords_real_path)
        self.stopwords = [stopword.strip("\n") for stopword in f.readlines()]

    def translate(self, word):
        if word in self.stopwords:
            return word

        word = self.lingo.translate(word)

        try:
            return self.cache[word]
        except:
            concepts = self.get_concepts(word)
            self.cache[word] = concepts
            return concepts

    def get_concepts(self, word):
        output = subprocess.check_output([BABELNET_SHELL, BABELNET_SCRIPT, 
            BABELNET_CONCEPTS_OPTION, word])

        concepts = output.split("\n")
        concepts = concepts[concepts.index("===DIVIDER===") + 1:-1]

        return " ".join(concepts)


    
