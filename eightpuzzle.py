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

        # Getting the second row
        row2 = input('Enter the second row, use spaces between numbers: ')

        # Getting the third row
        row3 = input('Enter the third row, use spaces between numbers: \n')

        row1 = row1.split(' ')
        row2 = row2.split(' ')
        row3 = row3.split(' ')

        puzzle = row1, row2, row3

    # Allowing the user to choose heuristic
    algo = input('Enter your choice of algorithm \n1. Uniform Cost Search '
                 '\n2. A* with the Misplaced Tile heuristic. \n3. A* with the Manhattan distance heuristic\n')
    algo = int(algo)

    # Running the program and printing the output
    print(generalsearch(puzzle, algo))


# Function to illustrate all possible ways the 0 can be moved around legally
def expand(node, s):
    r = 0
    c = 0
    count = 0
    expansionarr = []

    # Looking for position of 0 in the puzzle
    for i in range(len(node.puzzle)):
        for j in range(len(node.puzzle)):
            if int(node.puzzle[i][j]) == 0:
                r = i
                c = j

    # If not on the first row, then we can move the 0 up (row-wise)
    if r > 0:
        up = copy.deepcopy(node.puzzle)
        temp = up[r][c]
        up[r][c] = up[r-1][c]
        up[r - 1][c] = temp

        # If we have already seen the puzzle before, there is no need to revisit it
        for i in s:
            if up == i.puzzle:
                count += 1
        if count == 0:
            expansionarr.append(up)
        count = 0

    # If not on the last row, then we can move the 0 down (row-wise)
    if r < len(node.puzzle)-1:
        down = copy.deepcopy(node.puzzle)
        temp = down[r][c]
        down[r][c] = down[r+1][c]
        down[r + 1][c] = temp

        # If we have already seen the puzzle before, there is no need to revisit it
        for i in s:
            if down == i.puzzle:
                count += 1
        if count == 0:
            expansionarr.append(down)
        count = 0

    # If not on the first column, then we can move the 0 to the left (column-wise)
    if c > 0:
        left = copy.deepcopy(node.puzzle)
        temp = left[r][c]
        left[r][c] = left[r][c-1]
        left[r][c-1] = temp

        # If we have already seen the puzzle before, there is no need to revisit it
        for i in s:
            if left == i.puzzle:
                count += 1
        if count == 0:
            expansionarr.append(left)
        count = 0

    # If not on the last column, then we can move the 0 to the right (column-wise)
    if c < len(node.puzzle)-1:
        right = copy.deepcopy(node.puzzle)
        temp = right[r][c]
        right[r][c] = right[r][c+1]
        right[r][c+1] = temp

        # If we have already seen the puzzle before, there is no need to revisit it
        for i in s:
            if right == i.puzzle:
                count += 1
        if count == 0:
            expansionarr.append(right)

    return expansionarr


# Main "driver" program inspired by the psuedocode in the assignment PDF
def generalsearch(problem, algo):

    # Variable definition
    #     'q' is our queue, seen is all the puzzles we've seen already, ncount is nodes visited,
    #      qsz tracks the size of the queue and mq tracks the max size of the queue at any time
    q = []
    seen = []
    ncount = -1
    qsz = 0
    mq = -1

    # Calculating heuristic based on the user inputted heuristic
    if algo == 1:
        h = 0
    if algo == 2:
        h = misplaced(problem)
    if algo == 3:
        h = manhattan(problem)

    # Creating the start node, with the puzzle, depth of 0, and heuristic. We then add the node to the queue
    # and list it in the seen array.
    n = node(problem, 0, h)
    q.append(n)
    seen.append(n)
    qsz +=1
    mq += 1

    # Loop until we finish solving a problem
    while True:

        # Sort the queue for the lowest h(n) + g(n)
        q = sort(q)

        if len(q) == 0:
            return 'Failure :('

        # Remove the first node, increase node visited count but decrease queue size
        nd = q.pop(0)
        ncount += 1
        qsz -= 1

        # If we make it to goal state print some data
        if goal(nd.puzzle):
            return ('Goal!! \n\nTo solve this problem the search algorithm expanded a total of ' +
                  str(ncount) + ' nodes.\nThe maximum number of nodes in the queue at any one time was '
                  + str(mq) + '.\nThe depth of the goal node was ' + str(nd.depth))

        # Skipping on the first occasion to allow it to first decide which node is best to expand
        if ncount != 0:
            print('The best state to expand with a g(n) = ' + str(nd.depth) + ' and h(n) = ' + str(nd.hcost)
                  + ' is...\n' + str(nd.puzzle) + '\tExpanding this node...\n')

        # Expand all possible states from the node popped off the queue and put them in an array
        exarr = expand(nd, seen)

        # Loop through the array and create nodes based on the expanded puzzles based on heuristics chosen
        # by the user. The depth is the depth of the parent node (node popped off queue + 1).
        for i in exarr:
            if algo == 1:
                n = node(i, nd.depth + 1, 0)
            elif algo == 2:
                n = node(i, nd.depth + 1, misplaced(i))
            elif algo == 3:
                n = node(i, nd.depth + 1, manhattan(i))
            # Add these states to the queue and add them to a list of states we have now seen
            q.append(n)
            seen.append(n)
            qsz += 1

        # Change the max queue size if it has been surpassed
        if qsz > mq:
            mq = qsz


# Simple selection sort, if there is a tie it favors the node with the lower depth g(n)
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


# Go through the goal puzzle and sum the # of moves needed to return pieces 1-9 to their original spot
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


# Count how many tiles are not in the same place (not including the 0 tile)
def misplaced(puzzle):
    goal_pzl = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    count = 0

    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if int(puzzle[i][j]) != goal_pzl[i][j] and int(puzzle[i][j]) != 0:
                count += 1
    return count


# Check if the input puzzle matches the goal puzzle
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


# Node definition, stores puzzle, depth, and heuristic cost
class node:
    def __init__(self, puzzle, depth, hcost):
        self.puzzle = puzzle
        self.hcost = hcost
        self.depth = depth


if __name__ == "__main__":
    main()

