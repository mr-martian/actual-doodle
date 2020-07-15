#!/usr/bin/python3

debug = False

import sys
import random
import string
from streamparser import parse, mainpos, reading_to_string


class NoCandidatesForReplacement(Exception):
    pass


class NoReplacement(Exception):
    pass


random_flag = 0
idioms_list = open('eng-idioms-analysed.txt', 'r').read().split('\n')


def malaphor(input_idiom):
    replacement_candidates = []
    candidate_tags = ['n', 'adj', 'adv', 'vblex', 'v']

    #Parse Input Idiom to get a candidate for replacement
    lu_count = 0
    input_idiom_surface = []

    for lu in parse(input_idiom): 
        analyses = lu.readings
        firstreading = analyses[0]
        surfaceform = lu.wordform

        input_idiom_surface.append(surfaceform)

        if debug:
            print(firstreading[0].tags)
            print("^{}/{}$".format(surfaceform, 
                                   reading_to_string(firstreading)))
        
        for tag in candidate_tags:
            if tag in firstreading[0].tags:
                replacement_candidates.append([firstreading[0], surfaceform, lu_count])

        lu_count += 1

    if debug:
        print(replacement_candidates)

    if len(replacement_candidates) < 1:
        raise NoCandidatesForReplacement()

    elif len(replacement_candidates) == 1:
        final_replacement_candidate = replacement_candidates[0]

    else:
        final_replacement_candidate = replacement_candidates[random.randint(0,len(replacement_candidates)-1)]

    if debug:
        print("Final Replacement Candidate:")
        print(final_replacement_candidate)

    #Parse Idioms list (analysed through the tagger) to find a suitable replacement

    possible_replacements = []

    for idiom in idioms_list:
        for lu in parse(idiom):
            if lu.readings[0][0].tags == final_replacement_candidate[0].tags:
                possible_replacements.append([lu.readings[0][0], lu.wordform])

    replacement_flag = 1

    if len(possible_replacements) < 1:
        raise NoReplacement()

    elif len(possible_replacements) == 1:
        final_replacement_word = possible_replacements[0]

    else:
        final_replacement_word = possible_replacements[random.randint(0,len(possible_replacements)-1)]

    if debug:
        print("Replacement Word:")
        print(final_replacement_word)

    #Make the replacement in the original idiom
    pos = final_replacement_candidate[2] #contains the original position of the word in the input idiom

    if debug:
        print(input_idiom_surface)

    input_idiom_surface[pos] = final_replacement_word[1]

    if debug:
        print(input_idiom_surface)

    out = ''

    for word in input_idiom_surface:
        if out != '' and word[0] in string.ascii_letters:
            out += ' ' + word
        else:
            out += word
    return out.capitalize()


if __name__ == '__main__':
    if len(sys.argv) > 2:
        sys.stderr.write("Too many Args!\n")
        sys.exit(3)

    if len(sys.argv) == 2 and sys.argv[1] == '-r':
        random_flag = 1
        input_idiom = idioms_list[random.randint(0,len(idioms_list)-1)]

    else:
        input_idiom = sys.stdin.read()
    
    try:
        print(malaphor(input_idiom))
    except NoCandidatesForReplacement:
        sys.stderr.write("Sorry! Input idiom has no candidates for replacement! :( Try a different one.\n")
        sys.stderr.write("NOTE: This could be because Apertium recognises this idiom and hence doesn't provide analyses for the words.\n")
        sys.exit(1)
    except NoReplacement:
        sys.stderr.write("Didnt find any adequate replacement sorry! Try again :)\n")
        sys.exit(2)

    sys.exit(0)
