import sys
NULL = 0
DIAGONAL, UP, LEFT = 1, 2, 4
DIAUP, DIALEFT = 3, 5

class Element :
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


class GlobalAlignment :

    def __init__(self, seq1, seq2, match, mismatch, indel) :
        self.seq1 = seq1
        self.seq2 = seq2
        self.match = match
        self.mismatch = mismatch
        self.indel = indel
        self.table = [[Element(0) for x in range(len(seq1))] for y in range(len(seq2))]
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

    def align(self):

    def backtrack(self, x, y, aligned1, aligned2):

        while x > 0 and y > 0 :
            direction = self.table[x][y].getDirection()

            if direction == DIAGONAL :
                aligned1 += self.seq1[x]
                aligned2 += self.seq2[y]
                self.backtrack(x-1, y-1, aligned1, aligned2)

            elif direction == LEFT :
                aligned1 += self.seq1[x]
                aligned2 += '-'
                self.backtrack(x-1, y, aligned1, aligned2)

            elif direction == UP :
                aligned1 += '-'
                aligned2 += self.seq2[y]
                self.backtrack(x, y-1, aligned1, aligned2)

            elif direction == DIALEFT :

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
