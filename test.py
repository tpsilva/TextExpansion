import expansion.dictionary
import expansion.expansion

expansion.expansion.expand(["how r u"], (True, True, True, True))
expansion.expansion.expand(["lemme noe when u get der"], (True, True, True, True))


#ldic = expansion.dictionary.LingoDictionary()
#print ldic.translate("r")
#print ldic.translate("u")
#
#cdic = expansion.dictionary.ConceptsDictionary()
#print cdic.translate("car")
#
## check if cache is working
#print cdic.translate("car")
#
## check if stopwords are working
#print cdic.translate("you")
#
#ddic = expansion.dictionary.DisambiguationDictionary()
#ddic.init_concepts("this is a TEST")
#
#print ddic.translate("test")
#print ddic.translate("TEST")

