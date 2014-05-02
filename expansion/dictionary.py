

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
