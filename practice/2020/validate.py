import sys

TOTAL_LBLS = ['books', 'libraries', 'days']
LIB_LBLS = ['books', 'signup', 'ship']

def readInput(filename):
    def line2nums(line):
        return [int(c) for c in line.split(' ')]
    f = open(filename, "r")
    lines = filter(lambda x: x.strip(), f.readlines())
    return [line2nums(l.rstrip()) for l in lines]

def buildInput(filename):
    lines = readInput(filename)

    totals = { TOTAL_LBLS[i]:val for (i, val) in enumerate(lines[0]) }
    scores = lines[1]

    libraries = []
    for i in range(2, len(lines), 2):
        totals_lib = { LIB_LBLS[j]:val for (j, val) in enumerate(lines[i]) }
        print(i)
        books = lines[i+1]
        libraries.append({'books': books, 'totals': totals_lib})

    return (totals, scores, libraries)

def readOutput(filename):
    def line2nums(line):
        if line == '':
            return []
            
        return [int(c) for c in line.split(' ')]
    f = open(filename, "r")
    lines = map(lambda x: x.strip(), f.readlines())
    return [line2nums(l.rstrip()) for l in lines]

def buildOutput(filename):
    lines = readOutput(filename)
    lib_2_sign = lines[0][0]

    ret = []

    for l in range(lib_2_sign):
        print(2*l)
        (id, num) = (lines[2*l+1])
        books = lines[2*l+2]

        ret.append({'id': id, 'books': books})

    return ret

def check(filename_in, filename_out):
    print("checking input: '%s' with output: '%s'" % (filename_in, filename_out))
    (totals, scores, libraries) = buildInput(filename_in)
    output = buildOutput(filename_out)
    
    ids = { item['id'] for item in output}

    #no repeated library ids
    assert(len(ids) == len(output))

    #signed up libraries should be less or equal to the totals
    assert(len(output) <= totals['libraries'])

    #ids for libraries signed up should be in input
    for id in ids:
        assert(id < totals['libraries'])

    #books for each lib in output should be avail in that lib in input
    for item in output:
        lib = item['id']
        books = set(item['books'])
        #check no repeated ids
        assert(len(books) == len(item['books']))
        #check all books in output are in the library in the input file
        in_books = set(libraries[lib]['books'])

        #check all books in output are in input for that lib
        diff = books.difference(in_books)
        assert(len(diff) == 0)

    total_days = totals['days']
    start = 0
    #check than given the days constraints (sequential signups) each lib could scan that amount of books
    for item in output:
        lib = item['id']
        books = item['books']
        start += libraries[lib]['totals']['signup']
        
        ship = libraries[lib]['totals']['ship']
        avail_days = total_days - start - 1 #the 1 is for the scanning delay

        assert(avail_days*ship >= len(books))

    #nice to have: check no books are repeated between libs (would not count more than once for the score)
    all_books = []
    for item in output:
        books = item['books']
        all_books.extend(books)

    assert(len(all_books) == len(set(all_books)))
    print('all checks passed')

    #calculate total score
    all_scores = map(lambda book: scores[book], all_books)
    total_score = reduce(lambda b1, b2: b1+b2, all_scores)
    print("the total score is: %d" %(total_score))


assert(len(sys.argv) == 3)
check(sys.argv[1], sys.argv[2])