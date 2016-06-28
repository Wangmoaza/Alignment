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

class AlignedSeq :

    def __init__(self, seq1, seq2):
        self.seq1 = seq1
        self.seq2 = seq2

    def addToBoth(self, nt1, nt2):
        self.seq1 += nt1
        self.seq2 += nt2

class GlobalAlignment :

    def __init__(self, seq1, seq2, match, mismatch, indel) :
        self.seq1 = seq1
        self.seq2 = seq2
        self.match = match
        self.mismatch = mismatch
        self.indel = indel
        self.table = [[MatElement(0) for x in range(len(seq1))] for y in range(len(seq2))]
        self.construct_matrix() # construct matrices
    ### end - __init__

    def construct_matrix(self):
        # initialization
        for x in range(1, len(self.seq1)) :
            self.table[0][x].setScore(self.table[0][x-1].getScore() + self.indel)
            self.table[0][x].setDirection(LEFT)

        for y in range(1, len(self.seq2)) :
            self.table[y][0].setScore(self.table[y][0].getScore() + self.indel)
            self.table[y][0].setDirection(UP)

        # construct matrices
        for y in range(len(self.seq2)) :
            for x in range(len(self.seq1)) :
                # construct scoreMatrix
                if self.seq1[x] == self.seq2[y] :
                    match = self.table[x-1][y-1].getScore() + self.match
                else :
                    match = self.table[x-1][y-1].getScore() + self.mismatch

                insert = self.table[x-1][y].getScore() + self.indel
                delete = self.table[x][y-1].getScore() + self.indel

                maxScore = max([match, insert, delete])
                self.table[x][y].setScore(maxScore)

                # construct trackMatrix
                if maxScore == match :
                    if match == insert :
                        self.table[x][y].setDirection(DIALEFT)
                    elif match == delete :
                        self.table[x][y].setDirection(DIAUP)
                    else :
                        self.table[x][y].setDirection(DIAGONAL)

                elif maxScore == insert :
                    self.table[x][y].setDirection(LEFT)

                else :
                    self.table[x][y].setDirection(UP)
            ### end - for x
        ### end - for y
    ### end - def construct_matrix

    def backtrack(self, x, y):
        direction = self.table[x][y].getDirection()
        newSet = set()

        # base cases
        if x == 0 and y == 0 :
            return { AlignedSeq("", "") }

        elif x == 0 :
            return { AlignedSeq("-" * y, self.seq2[:y]) }

        elif y == 0 :
            return { AlignedSeq(self.seq1[:x], "-" * x) }

        # recursive
        elif direction == DIAGONAL :
            return { item.addToBoth(self.seq1[x], self.seq2[y]) for item in backtrack(x-1, y-1) }

        elif direction == LEFT :
            return { item.addToBoth(self.seq1[x], "-") for item in backtrack(x-1, y) }

        elif direction == UP :
            return { item.addToBoth("-", self.seq2[y]) for item in backtrack(x, y-1) }

        elif direction == DIALEFT :
            newSet.update(backtrack())
            pass

        elif direction == DIAUP :
            pass

def main():
    inputStr = input()
    args = inputStr.split()

    if len(args) != 5:
        print("Wrong number of arguments")
        sys.exit()

    seq1, seq2 = args[0], args[1]
    match, mismatch, indel = int(args[2]), int(args[3]), int(args[4])


main()
