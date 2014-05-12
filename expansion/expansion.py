import re

import dictionary

LINGO = 0
ORIGINAL = 1
CONCEPTS = 2
DISAMBIGUATION = 3

def should_append(original_added, token, translation):
    return translation != token or not original_added

def expand(samples, parameters, *dictionary_filenames):
    dictionaries = range(4) # check if there's a better way to create the list
    dictionaries[LINGO] = dictionary.LingoDictionary()
    dictionaries[ORIGINAL] = None
    dictionaries[CONCEPTS] = dictionary.ConceptsDictionary()
    dictionaries[DISAMBIGUATION] = dictionary.DisambiguationDictionary()

    custom_dictionaries = []
    for dictionary_filename in dictionary_filenames:
        custom_dictionaries = dictionary.GenericDictionary(dictionary_filename)

    translated_samples = []
    for sample in samples:
        translated_sample = []
        
        dictionaries[DISAMBIGUATION].init_concepts(sample)

        for token in re.split("[\t\ ]", sample):
            original_added = False

            if parameters[ORIGINAL]:
                translated_sample.append(token)
                original_added = True

            if parameters[LINGO]:
                lingo_translation = dictionaries[LINGO].translate(token)
                if should_append(original_added, token, lingo_translation):
                    translated_sample.append(lingo_translation)

            if parameters[CONCEPTS] and not parameters[DISAMBIGUATION]:
                concepts_translation = dictionaries[CONCEPTS].translate(token)
                if should_append(original_added, token, concepts_translation):
                    translated_sample.append(concepts_translation)

            if parameters[DISAMBIGUATION]:
                disambiguation_translation = dictionaries[DISAMBIGUATION].translate(token)
                if should_append(original_added, token, disambiguation_translation):
                    translated_sample.append(disambiguation_translation)

        print " ".join(translated_sample)