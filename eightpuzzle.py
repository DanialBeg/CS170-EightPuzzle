import copy

def main():
    print('Welcome to Danial\'s 8 puzzle solver!')

    # Getting user input for if they want to use default or their own
    inputsel = input('Please type “1” to use a default puzzle, or “2” to enter your own puzzle!'
                     ' Please be sure to press ENTER after making your choice!\n')
    inputnum = int(inputsel)

    # Setting up puzzle if user uses a custom puzzle
    if inputnum == 1:
        puzzle = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
    if inputnum == 2:
        print('Enter your puzzle, use a zero to represent the blank \n')

        # Getting the first row
        row1 = input('Enter the first row, use spaces between numbers: ')
        row1 = row1.split(' ')

        # Getting the second row
        row2 = input('Enter the second row, use spaces between numbers: ')
        row2 = row2.split(' ')

        # Getting the third row
        row3 = input('Enter the third row, use spaces between numbers: ')
        row3 = row3.split(' ')

        print('\n')

        puzzle = row1, row2, row3

    algo = input('Enter your choice of algorithm \n1. Uniform Cost Search '
                 '\n2. A* with the Misplaced Tile heuristic. \n3. A* with the Manhattan distance heuristic\n')
    algo = int(algo)

    print(generalsearch(puzzle, algo))


def expand(node, s):
    r = 0
    c = 0
    count = 0
    expansionarr = []
    # seenset = set()
    # for l in range(len(s)):
    #         seenset.add(s[l].puzzle)

    for i in range(len(node.puzzle)):
        for j in range(len(node.puzzle)):
            if int(node.puzzle[i][j]) == 0:
                r = i
                c = j

    if r > 0:
        up = copy.deepcopy(node.puzzle)
        temp = up[r][c]
        up[r][c] = up[r-1][c]
        up[r - 1][c] = temp
        for i in s:
            if up == i.puzzle:
                count += 1
        if count == 0:
            expansionarr.append(up)
        count = 0
    if r < len(node.puzzle)-1:
        down = copy.deepcopy(node.puzzle)
        temp = down[r][c]
        down[r][c] = down[r+1][c]
        down[r + 1][c] = temp
        for i in s:
            if down == i.puzzle:
                count += 1
        if count == 0:
            expansionarr.append(down)
        count = 0
    if c > 0:
        left = copy.deepcopy(node.puzzle)
        temp = left[r][c]
        left[r][c] = left[r][c-1]
        left[r][c-1] = temp
        for i in s:
            if left == i.puzzle:
                count += 1
        if count == 0:
            expansionarr.append(left)
        count = 0
    if c < len(node.puzzle)-1:
        right = copy.deepcopy(node.puzzle)
        temp = right[r][c]
        right[r][c] = right[r][c+1]
        right[r][c+1] = temp
        for i in s:
            if right == i.puzzle:
                count += 1
        if count == 0:
            expansionarr.append(right)
        count = 0

    # print(expansionarr)
    return expansionarr


def generalsearch(problem, algo):
    q = []
    seen = []
    ncount = -1
    qsz = 0
    mq = -1

    if algo == 1:
        h = 0
    if algo == 2:
        h = misplaced(problem)
    if algo == 3:
        h = manhattan(problem)
    n = node(problem, 0, h)
    q.append(n)
    seen.append(n)
    qsz +=1
    mq += 1

    while True:
        if len(q) == 0:
            return 'Failure :('
        nd = q.pop(0)
        ncount += 1
        qsz -= 1

        if goal(nd.puzzle):
            return ('Goal!! \n\nTo solve this problem the search algorithm expanded a total of ' +
                  str(ncount) + ' nodes.\nThe maximum number of nodes in the queue at any one time was '
                  + str(mq) + '.\nThe depth of the goal node was ' + str(nd.depth))

        if ncount != 0:
            print('The best state to expand with a g(n) = ' + str(nd.depth) + ' and h(n) = ' + str(nd.hcost)
                  + ' is...\n' + str(nd.puzzle) + '\tExpanding this node...\n')

        exarr = expand(nd, seen)

        for i in exarr:
            if algo == 1:
                n = node(i, nd.depth + 1, 0)
            elif algo == 2:
                n = node(i, nd.depth + 1, misplaced(i))
            elif algo == 3:
                n = node(i, nd.depth + 1, manhattan(i))
            q.append(n)
            seen.append(n)
            # ncount += 1
            qsz += 1
        if qsz > mq:
            mq = qsz
        q = sort(q)


def sort(queue):
    for i in range(len(queue)):
        for j in range(i+1, len(queue)):
            if queue[i].depth + queue[i].hcost > queue[j].depth + queue[j].hcost:
                temp = queue[i]
                queue[i] = queue[j]
                queue[j] = temp
            if queue[i].depth + queue[i].hcost == queue[j].depth + queue[j].hcost:
                if queue[i].depth > queue[j].depth:
                    temp = queue[j]
                    queue[j] = queue[i]
                    queue[i] = temp
    return queue


def manhattan(puzzle):
    goal_pzl = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    count = 0
    gr, gc, r, c = 0, 0, 0, 0

    for l in range(1, 9):
        for i in range(len(puzzle)):
            for j in range(len(puzzle)):
                if int(puzzle[i][j]) == l:
                    r = i
                    c = j
                if goal_pzl[i][j] == l:
                    gr = i
                    gc = j
        count += abs(gr-r) + abs(gc-c)

    return count


def misplaced(puzzle):
    goal_pzl = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    count = 0

    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if int(puzzle[i][j]) != goal_pzl[i][j] and int(puzzle[i][j]) != 0:
                count += 1
    return count


def goal(puzzle):
    goal_pzl = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    count = 0

    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if int(puzzle[i][j]) != goal_pzl[i][j]:
                count += 1
    if count > 0:
        return False
    return True


class node:
    def __init__(self, puzzle, depth, hcost):
        self.puzzle = puzzle
        self.hcost = hcost
        self.depth = depth


if __name__ == "__main__":
    main()

