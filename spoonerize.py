#!/usr/bin/python3

import sys

in_word = False
in_blank = False

cur = ''

word_buffer = []
current_word = ''

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
    if s1[0].lower() in 'aeiou':
        print(s1 + word_buffer[1], end='')
        word_buffer = word_buffer[2:]
        return
    if s2[0].lower() in 'aeiou':
        word_buffer[1] += s2
        word_buffer = word_buffer[:2]
        return
    p1 = ''
    p2 = ''
    while s1[0].lower() not in 'aeiou':
        p1 += s1[0]
        s1 = s1[1:]
    while s2[0].lower() not in 'aeiou':
        p2 += s2[0]
        s2 = s2[1:]
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
