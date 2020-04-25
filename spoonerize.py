#!/usr/bin/python3

import sys

in_word = False
in_blank = False

cur = ''

word_buffer = []
current_word = ''

def split_prefix(s):
    for i, c in enumerate(s.lower()):
        if c in 'aeiou':
            return s[:i], s[i:]
        elif i > 0 and c == 'y':
            return s[:i], s[i:]
    return '', s

def spoonerize():
    global word_buffer
    #print(word_buffer)
    w1 = word_buffer[0]
    w2 = word_buffer[2]
    s1 = w1[1:].split('/')[0]
    s2 = w2[1:].split('/')[0]
    tags = ['<n>', '<adj>', '<adv>', '<vblex>', '<v>']
    for t in tags:
        if t in w1:
            break
    else:
        print(s1 + word_buffer[1], end='')
        word_buffer = word_buffer[2:]
        return
    for t in tags:
        if t in w2:
            break
    else:
        word_buffer[1] += s2
        word_buffer = word_buffer[:2]
        return
    p1, s1 = split_prefix(s1)
    if p1 == '':
        print(s1 + word_buffer[1], end='')
        word_buffer = word_buffer[2:]
        return
    p2, s2 = split_prefix(s2)
    if p2 == '':
        word_buffer[1] += s2
        word_buffer = word_buffer[:2]
        return
    print(p2 + s1 + word_buffer[1] + p1 + s2, end='')
    word_buffer = []

while True:
    cur = sys.stdin.read(1)
    if not cur:
        break
    if in_blank:
        current_word += cur
        if cur == ']':
            in_blank = False
    elif not in_word:
        if cur == '^':
            in_word = True
            if len(word_buffer) == 1:
                word_buffer.append(current_word)
            elif len(word_buffer) == 2:
                word_buffer[1] += current_word
            else:
                print(current_word, end='')
            current_word = cur
        else:
            current_word += cur
            if cur == '[':
                in_blank = True
    else:
        current_word += cur
        if cur == '$':
            in_word = False
            word_buffer.append(current_word)
            current_word = ''
            if len(word_buffer) == 3:
                spoonerize()

if current_word:
    word_buffer.append(current_word)
if len(word_buffer) == 3:
    spoonerize()
for w in word_buffer:
    if w[0] == '^':
        print(w[1:].split('/')[0], end='')
    else:
        print(w, end='')
