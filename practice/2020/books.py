#!/bin/python

import sys
import random
import math

TOTAL_LBLS = ['books', 'libraries', 'days']
LIB_LBLS = ['books', 'signup', 'ship']

def line2nums(line):
    return [int(c) for c in line.split(' ')]

def readFile(filename):
    f = open(filename, "r")
    lines = filter(lambda x: x.strip(), f.readlines())
    return [line2nums(l.rstrip()) for l in lines]

def buildInput(filename):
    lines = readFile(filename)

    totals = { TOTAL_LBLS[i]:val for (i, val) in enumerate(lines[0]) }
    scores = lines[1]

    libraries = []
    for i in range(2, len(lines), 2):
        totals_lib = { LIB_LBLS[j]:val for (j, val) in enumerate(lines[i]) }
        # books = lines[i+1]
        books = sorted(lines[i+1], key=lambda b: scores[b], reverse=True) 
        libraries.append({'books': books, 'totals': totals_lib})

    return (totals, scores, libraries)

def stratFirst(count, actives, libraries, scores, days_left, scanned, shipped, T):
    for i in range(0, count):
        if i not in actives:
            return i
    return None

def stratLast(count, actives, libraries, scores, days_left, scanned, shipped, T):
    for i in range(count-1, -1, -1):
        if i not in actives:
            return i
    return None

def stratGreedy(count, actives, libraries, scores, days_left, scanned, shipped, T):
    best = None
    mx = -1
    for i in range(0, count):
        if i not in actives:
            book = libraries[i]['books'][0]
            val = scores[book]
            if val > mx:
                best = i
                mx = val
    return best

def stratGenerous(count, actives, libraries, scores, days_left, scanned, shipped, T):
    best = None
    mn = None 
    for i in range(0, count):
        if i not in actives:
            book = libraries[i]['books'][0]
            val = scores[book]
            if mn == None or val < mn:
                best = i
                mn = val
    return best

def stratEdu(count, actives, libraries, scores, days_left, scanned, shipped, T):
    best = None
    mx = -1

    for i in range(0, count):
        if i not in actives:
            signup = libraries[i]['totals']['signup']
            ship = libraries[i]['totals']['ship']
            count = 0
            val = 0
            total = (days_left-signup)*ship

            for book in libraries[i]['books']:
                if (book not in scanned) and (book not in shipped) and (count < total):
                    val += scores[book]
                    count += 1
            if val > mx:
                mx = val
                best = i

    return best

def stratSimAnnealing(count, actives, libraries, scores, days_left, scanned, shipped, T):
    def p(e, e1, T):
        if e1 > e: return 1
        return math.exp(-(e-e1)/T)

    best = None
    mx = -1

    for i in range(0, count):
        if i not in actives:
            signup = libraries[i]['totals']['signup']
            ship = libraries[i]['totals']['ship']
            count = 0
            val = 0
            total = (days_left-signup)*ship

            for book in libraries[i]['books']:
                if (book not in scanned) and (book not in shipped) and (count < total):
                    val += scores[book]
                    count += 1
            if p(mx, val, T) >= random.uniform(0, 1):
                mx = val
                best = i

    return best

def writeOutput(filename, res, arr_actives):
    def writeArrInts(f, v):
        v = map(lambda x: str(x), v)
        s = ' '.join(v)
        f.write(s + "\n")

    f = open(filename.replace(".txt", ".out"), "w")

    writeArrInts(f, [len(arr_actives)])
    for lib in arr_actives:
        books = res[lib]
        writeArrInts(f, [lib, len(books)])
        writeArrInts(f, books)
    
    f.close()

def solve(filename, stratFunc):
    print("solving for: " +  filename)
    (totals, scores, libraries) = buildInput(filename)

    actives = {}
    signup = {'left': 0, 'library': None}
    scanned = {}
    shipped = {}
    arr_actives = []

    res = { lib:[] for lib in range(totals['libraries']) }

    for day in range(totals['days']):
        T = (day+1)/float(totals['days'])
        if day > 100 and day % 100 == 0:
            print('day', day, '/', totals['days'])
        if signup['left'] == 0:
            if signup['library'] != None and signup['library'] not in actives:
                actives[signup['library']] = 1
                arr_actives.append(signup['library'])
            lib = stratFunc(totals['libraries'], actives, libraries, scores, totals['days'] - day, scanned, shipped, T)
            if lib != None:
                signup = {'left': libraries[lib]['totals']['signup']-1, 'library': lib}
        else:
            signup['left'] -= 1

        for (b, lib) in shipped.items():
            scanned[b] = lib
            #books scanned for a lib might not return in order
            res[lib].append(b)

        shipped = {}

        #picking the best lib to start with could be an optimization
        for lib in actives:
            library = libraries[lib]
            ship = library['totals']['ship']
            count = 0
            for b in library['books']:
                if (b not in scanned) and (b not in shipped) and count < ship:
                    shipped[b] = lib
                    count += 1

    scanned = scanned.keys()
    costs = [scores[b] for b in scanned]
    cost = sum(costs)
    print(cost)
    # print(res)
    # print(actives)

    writeOutput(filename, res, arr_actives)

assert(len(sys.argv) == 2)

filename = sys.argv[1]
solve(filename, stratEdu)