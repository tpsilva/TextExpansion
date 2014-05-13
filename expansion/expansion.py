import re

import dictionary

LINGO = 0
ORIGINAL = 1
CONCEPTS = 2
DISAMBIGUATION = 3

def init_dictionaries():
    dictionaries = range(4) # check if there's a better way to create the list

    dictionaries[LINGO] = dictionary.LingoDictionary()
    dictionaries[ORIGINAL] = None
    dictionaries[CONCEPTS] = dictionary.ConceptsDictionary()
    dictionaries[DISAMBIGUATION] = dictionary.DisambiguationDictionary()

    return dictionaries

def init_custom_dictionaries(dictionary_filenames):
    custom_dictionaries = []

    for dictionary_filename in dictionary_filenames:
        custom_dictionaries.append(dictionary.GenericDictionary(dictionary_filename))

    return custom_dictionaries


def translate(token, dictionary, expanded_sample):
    translation = dictionary.translate(token)
    if translation not in expanded_sample:
        expanded_sample.append(translation)

def expand(samples, parameters, *dictionary_filenames):
    dictionaries = init_dictionaries()
    custom_dictionaries = init_custom_dictionaries(dictionary_filenames)

    expanded_samples = []
    for sample in samples:
        expanded_sample = []
        
        if parameters[DISAMBIGUATION]: # only init disambiguation when needed
            dictionaries[DISAMBIGUATION].init_concepts(sample)

        for token in re.split("[\t\ ]", sample.lower()):

            if parameters[ORIGINAL]:
                expanded_sample.append(token)

            if parameters[LINGO]:
                translate(token, dictionaries[LINGO], expanded_sample)

            if parameters[CONCEPTS] and not parameters[DISAMBIGUATION]:
                translate(token, dictionaries[CONCEPTS], expanded_sample)

            if parameters[DISAMBIGUATION]:
                translate(token, dictionaries[DISAMBIGUATION], expanded_sample)

            for custom_dictionary in custom_dictionaries:
                translate(token, custom_dictionary, expanded_sample)

        expanded_samples.append(" ".join(expanded_sample))

    print "\n".join(expanded_samples)
