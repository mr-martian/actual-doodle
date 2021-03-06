#!/usr/bin/python3

debug = False 

import sys
import random
import string
import argparse
import os
import subprocess
import io
from streamparser import parse, mainpos, reading_to_string


class NoCandidatesForReplacement(Exception):
    pass


class NoReplacement(Exception):
    pass


random_flag = 0


def malaphor(input_idiom, lang):
    idioms_list = open(f'{lang}-idioms-analysed.txt', 'r').read().split('\n')
    replacement_candidates = []
    candidate_tags = ['n', 'adj', 'adv', 'vblex', 'v']

    #Parse Input Idiom to get a candidate for replacement
    lu_count = 0
    input_idiom_surface = []

    for lu in parse(input_idiom): 
        if debug:
            print(lu)
        analyses = lu.readings
        if debug:
            print(analyses)
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

    #Parse Idioms list (analysed through the morph) to find a suitable replacement

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
        if out != '' and word[0] in string.ascii_letters + string.digits:
            out += ' ' + word
        else:
            out += word
    return out.capitalize()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lang', help='Language to use as three letter code, defaults to eng (can also be specified with env var APERTIUM_LANG)', default='envvar')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--path', help='Path to Apertium monolingual package (can also be specified with env var APERTIUM_XYZ e.g. APERTIUM_ENG)')
    group.add_argument('-i', '--installed', help='Apertium monolingual package is installed with packaging (default)', action='store_true')
    group.add_argument('-r', '--random', help='Ignore stdin and generate a random malaphor (does not need apertium)', action='store_true')
    group.add_argument('-a', '--analysed', help='stdin has already been analysed', action='store_true')
    args = parser.parse_args()

    lang = args.lang
    if lang == 'envvar':
        try:
            lang = os.environ['APERTIUM_LANG']
        except KeyError:
            lang = 'eng'
            
    idioms_list = open(f'{lang}-idioms-analysed.txt', 'r').read().split('\n')

    if args.random:
        random_flag = 1
        input_idiom = idioms_list[random.randint(0,len(idioms_list)-1)]
    else:
        input_idiom = sys.stdin.read()
        if not args.analysed:
            if args.installed:
                command = ['apertium', f'{lang}-morph',]
            elif args.path:
                command = ['apertium', '-d', args.path, f'{lang}-morph',]
            else:
                try:
                    command = ['apertium', '-d', os.environ[f'APERTIUM_{lang.upper()}'], f'{lang}-morph',]
                except KeyError:
                    command = ['apertium', f'{lang}-morph',]
            proc = subprocess.run(command, universal_newlines=True, input=input_idiom, stdout=subprocess.PIPE)
            input_idiom = proc.stdout
    
    try:
        print(malaphor(input_idiom, lang))
    except NoCandidatesForReplacement:
        sys.stderr.write("Sorry! Input idiom has no candidates for replacement! :( Try a different one.\n")
        sys.stderr.write("NOTE: This could be because Apertium recognises this idiom and hence doesn't provide analyses for the words.\n")
        sys.exit(1)
    except NoReplacement:
        sys.stderr.write("Didnt find any adequate replacement sorry! Try again :)\n")
        sys.exit(2)

    sys.exit(0)
