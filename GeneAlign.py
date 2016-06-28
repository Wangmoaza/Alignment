import sys
NULL = 0
DIAGONAL, UP, LEFT = 1, 2, 4
DIAUP, DIALEFT = 3, 5

class MatElement :
    def __init__(self, score):
        self.score = score
        self.direction = NULL
        self.visited = False

    def setScore(self, score):
        self.score = score

    def setDirection(self, direction):
        self.direction = direction

    def getScore(self):
        return self.score

    def getDirection(self):
        return self.direction

    def visit(self):
        self.visited = True

    def isVisited(self):
        return self.visited

    def __str__(self):
        return "S:{0} D:{1}".format(self.score, self.direction)


class AlignedSeq :

    def __init__(self, seq1, seq2):
        self.seq1 = seq1
        self.seq2 = seq2

    def addToBoth(self, nt1, nt2):
        self.seq1 += nt1
        self.seq2 += nt2

    def __str__(self):
        return "{0}\n{1}".format(self.seq1, self.seq2)


class GlobalAlignment :

    def __init__(self, seq1, seq2, match, mismatch, indel) :
        self.seq1 = "-" + seq1
        self.seq2 = "-" + seq2
        self.match = match
        self.mismatch = mismatch
        self.indel = indel
        self.scoreMatrix = [ [ 0 for x in range(len(self.seq1)) ]  for y in range(len(self.seq2)) ]
        self.dirMatrix = [ [ NULL for x in range(len(self.seq1)) ]  for y in range(len(self.seq2)) ]
        self.construct_matrix() # construct matrices
    ### end - __init__

    def construct_matrix(self):
        # initialization
        for x in range(1, len(self.seq1)) :
            self.scoreMatrix[0][x] = self.scoreMatrix[0][x-1] + self.indel
            self.dirMatrix[0][x] = LEFT

        for y in range(1, len(self.seq2)) :
            self.scoreMatrix[y][0] = self.scoreMatrix[y-1][0] + self.indel
            self.dirMatrix[y][0] = UP

        # construct matrices
        for y in range(1, len(self.seq2)) :
            for x in range(1, len(self.seq1)) :

                # construct scoreMatrix
                if self.seq1[x] == self.seq2[y] :
                    match = self.scoreMatrix[y-1][x-1] + self.match
                else :
                    match = self.scoreMatrix[y-1][x-1] + self.mismatch

                insert = self.scoreMatrix[y-1][x] + self.indel
                delete = self.scoreMatrix[y][x-1] + self.indel

                maxScore = max([match, insert, delete])
                self.scoreMatrix[y][x] = maxScore

                # construct trackMatrix
                if maxScore == match :
                    if match == insert :
                        self.dirMatrix[y][x] = DIAUP
                    elif match == delete :
                        self.dirMatrix[y][x] = DIALEFT
                    else :
                        self.dirMatrix[y][x] = DIAGONAL

                elif maxScore == insert :
                    self.dirMatrix[y][x] = UP

                else :
                    self.dirMatrix[y][x] = LEFT
            ### end - for x
        ### end - for y

    ### end - def construct_matrix

    def backtrack(self, x, y):
        direction = self.dirMatrix[y][x]
        newSet = set()

        # base cases
        if x == 0 and y == 0 :
            return { AlignedSeq("", "") }

        # recursive
        elif direction == DIAGONAL :
            for item in self.backtrack(x-1, y-1) :
                item.addToBoth(self.seq1[x], self.seq2[y])
                newSet.add(item)
            return newSet

        elif direction == LEFT :
            for item in self.backtrack(x-1, y):
                item.addToBoth(self.seq1[x], "-")
                newSet.add(item)
            return newSet

        elif direction == UP :
            for item in self.backtrack(x, y-1):
                item.addToBoth("-", self.seq2[y])
                newSet.add(item)
            return newSet

        elif direction == DIALEFT :
            for item in self.backtrack(x - 1, y):   # left
                item.addToBoth(self.seq1[x], "-")
                newSet.add(item)

            for item in self.backtrack(x - 1, y - 1):
                item.addToBoth(self.seq1[x], self.seq2[y])
                newSet.add(item)

            return newSet

        elif direction == DIAUP :
            for item in self.backtrack(x, y - 1):    # up
                item.addToBoth("-", self.seq2[y])
                newSet.add(item)

            for item in self.backtrack(x - 1, y - 1):
                item.addToBoth(self.seq1[x], self.seq2[y])
                newSet.add(item)

            return newSet
    ### end - def backtrack

    def align(self):
        resultSet = self.backtrack(len(self.seq1) - 1, len(self.seq2) - 1)
        cnt = 1

        for item in resultSet :
            print("case {0}".format(cnt))
            print(item)
            cnt += 1
        ### end - for item
    # end - def align

def main():
    inputStr = input()
    args = inputStr.split()

    if len(args) != 5:
        print("Wrong number of arguments")
        sys.exit()

    seq1, seq2 = args[0], args[1]
    match, mismatch, indel = int(args[2]), int(args[3]), int(args[4])
    query = GlobalAlignment(seq1, seq2, match, mismatch, indel)
    query.align()

main()
