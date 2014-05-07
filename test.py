import expansion.dictionary

ldic = expansion.dictionary.LingoDictionary()
print ldic.translate("how r u")

cdic = expansion.dictionary.ConceptsDictionary()
print cdic.translate("car")

# check if cache is working
print cdic.translate("car")

# check if stopwords are working
print cdic.translate("you")

ddic = expansion.dictionary.DisambiguationDictionary()
ddic.init_concepts("this is a TEST")

print ddic.translate("test")
print ddic.translate("TEST")

