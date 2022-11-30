import sys #for sys.argv
import copy #for deepcopy method

# Begin Definitions

# Represents a node of an n-ary tree, depth of tree defined by depth argument in generateBoards
class Node :
    def __init__(self ,board):
        self.board = board
        self.children = [] # each Node can contain up to N children
        self.score = 0
        
# prints the game board
#
# @param board 2d array to be printed
# @return void
#
def printBoard(board):
    segment = '+---'
    line = ''
    for i in range(n):
        line+=segment
    line = line+'+'
    for i in range(n):
        print(line)
        for j in range(n):
            print('| '+board[i][j]+' ', end='')
        print('|')
    print(line)
    for i in range(n):
        if i < 9:
            print('| '+str(i+1)+' ', end='')
        else:
            print('| '+str(i+1)+'', end='') # omit trailing space so next | lines up
    print('|')
# end printBoard

# updates the game board by placing a marker into
# a specified column
#
# @param player 0 or 1 representing player
# @param c column in which to place a marker
# @param board 2d array to be updated
# @return void
#
def updateBoard(player, c, board):
    if player == 1:
        char = 'X'
    else:
        char = 'O'
    i = n-1
    while i != -1: #start at the bottom row, work up until find a blank space
        if board[i][c-1] == ' ':
            board[i][c-1] = char
            break
        else:
            i-=1
#end updateBoard

# return number of possible connectM's for a player and board state
# 
# @param n board dimension
# @param m desired number of pieces in a row
# @param player 0 or 1 representing player
# @param board 2d array containing board
# @param checkwin = '' to check for a winning board, ' ' otherwise
# @return void
#
def evalBoard (n, m, player, board, checkwin): 
    if player == 1:
        char = 'X'
    else:
        char = 'O'
    chars = [char, checkwin]
    total = 0
    # check rows
    for i in range(n):
        count = 0
        j = 0
        while j < n-m+1: # check each position until a connect m is no longer possible on that row
            while board[i][j] in chars:
                count +=1
                j+=1
                if count == m:
                    total+=1
                    count = 0
                    break
            else:
                count = 0
                j+=1
    # check columns
    for j in range(n):
        count = 0
        i = 0
        while i < n-m+1: # check each position until a connect m is no longer possible on that column
            while board[i][j] in chars:
                count +=1
                i+=1
                if count == m:
                    total+=1
                    count = 0
                    break
            else:
                count = 0
                i+=1
    # check down-right diagonal
    for i in range(n-m+1): #from first possible down-right diagonal to last
        for j in range(n-m+1):
            count = 0
            i2 = i
            while board[i2][j] in chars:
                count+=1
                if count == m:
                    total+=1
                    count = 0
                    break
                i2+=1
                j+=1
    # check down-left diagonal
    for i in range(n-m+1): #from first possible down-left diagonal to last
        for j in range(m-1,n):
            i2 = i
            count = 0
            while board[i2][j] in chars:
                count+=1
                if count == m:
                    total+=1
                    count = 0
                    break
                i2+=1
                j-=1
    return total
# end evalBoard

# recursive function that builds tree of game states
# 
# @param depth defines depth of tree
# @param node current node being evaluated/assigned children
# @param player 0 or 1 representing player
# @param n board dimension
# @param m desired number of pieces in a row
# @return 0 at depth 0, otherwise null
#
def generateBoards(calling_player, depth, node, player, n, m):
    if depth == 0: # weight winning boards very heavily, then add other possible connect-M boards
        node.score =  (evalBoard(n, m, calling_player, node.board, '') - evalBoard(n, m, calling_player%2+1, node.board, '')*10) * 100000
        node.score += evalBoard(n, m, calling_player, node.board, ' ') - evalBoard(n, m, calling_player%2+1, node.board, ' ')
        return 0
    else:
        offset = 0 # keeps recursive gB call from going out of range
        for i in range(n):
            if node.board[0][i] != ' ': #column is full
                offset+=1
            else:
                new_board = copy.deepcopy(node.board)
                updateBoard(player, i+1, new_board)
                node.children.append(Node(new_board))
                generateBoards(calling_player, depth-1, node.children[i-offset], player%2+1, n, m)
# end generateBoards

# determines best move by performing alpha-beta pruning on tree
# 
# @param depth level of traversal remaining
# @param node current node to evaluate
# @return array of best moves
#
def alphaBeta (depth, node):
    a = []
    alpha = -1000000
    beta = 1000000
    for i in range(len(node.children)):
        alpha1 = minValue_ab(depth-1, node.children[i], alpha, beta)
        if alpha1 > alpha:
            alpha = alpha1
            a.append(i)
    return a
# end alphaBeta

# determines min for minMax operation
# 
# @param depth level of traversal remaining
# @param node current node to evaluate
# @return min
#
def minValue_ab (depth, node, alpha, beta):
    if depth == 0:
        return node.score
    for i in range(len(node.children)):
        beta = min(beta, maxValue_ab(depth-1, node.children[i], alpha, beta))
        if (alpha >= beta):
            return -1000000
    return beta
# end minValue_ab

# determines max for minMax operation
# 
# @param depth level of traversal remaining
# @param node current node to evaluate
# @return max
#
def maxValue_ab (depth, node, alpha, beta):
    if depth == 0:
        return node.score
    for i in range(len(node.children)):
        alpha = max(alpha, minValue_ab(depth-1, node.children[i], alpha, beta))
        if (alpha >= beta):
            return 1000000
    return alpha
# end maxValue_ab

# End Defintions

# get and error-check command line arguments, set n m h
if (len(sys.argv) != 4):
    print('Number of arguments must be 3. Format: "python3 connectM n m h"')
    quit()
n = int(sys.argv[1])
m = int(sys.argv[2])
h = int(sys.argv[3])

if (n < 3 or n > 10):
    print('n must be at least 3 and less than 10')
    quit()
   
if (m <2 or m > n):
    print('m must be at least 2 and no higher than n')
    quit()
   
if (h < 0 or h > 1):
    print('h must be 0 for human and 1 for computer')
    quit()

# game setup and loop
if h == 0:
    first = 'computer'
else:
    first = 'human'

print('Starting an ' + str(n) + ' x ' + str(n) + ' game. You must connect ' + str(m) + ' in a row to win.')
print('The ' + first + ' will move first. The computer will use an X and is Player 1, the human will use an O and is Player 2.')

board = [[' ' for x in range(n)] for y in range(n)] # create and intialize 2d array for game board
moves = n*n # determine maximum number of moves
player = h + 1

possibleLookahead = [9, 7, 5, 5, 5, 4, 4, 4] # pre-defined look ahead values for different values of N

while (moves > 0): # loop until we run out of moves

    printBoard(board)

    if player == 2: # Human Player
        while True: # get and validate input
            try:
                c = int(input('It is player ' + str(player) + "'s turn. Please enter a column:"))
            except ValueError: # user entered something other than a number
                print('Please enter a number.')
                continue
            if c < 1 or c > n:
                print('Column must be between 1 and '+str(n))
                continue
            if board[0][c-1] != ' ': #column is full
                print('Column is full, pick another.')
                continue
            else:
                break
    # end if player == 2

    else: # computer choose last element in move array (best choice), corrected for available columns
        if moves == n * n: # first move, force computer to pick a middle columns
            c = int(n/2)+1
        else:
            root = Node(board) # Create root node of tree
            lookahead = possibleLookahead[n - 3]
            if moves < lookahead:
                lookahead = moves
            possible_moves = pow(n,lookahead)
            print("Computer is evaluating {:,} ".format(possible_moves)+"future boards")
            generateBoards(player, lookahead, root, player, n, m) # build rest of tree
            move = alphaBeta(lookahead, root) # traverse tree to determine best move
            best = len(move)
            if best == 0: # a returned empty, late game w only 1 leaf from root
                c = 1
            else:
                c = move[best-1]+1
            free = 0
            for i in range(n): # if columns are full, computer meant take the cth available column...
                if board[0][i] == ' ': 
                    free+=1
                    if free == c:
                        break
            c = i+1
        print('Computer chooses column ' +str(c))
    # end else

    updateBoard(player, c, board)

    if evalBoard(n, m, player, board, '') >= 1:
        print('Player ' + str(player)+ ' wins!')
        break

    player = player%2 +1 # swap player
    moves -=1

    if evalBoard(n, m, player, board, ' ') == 0 and evalBoard(n, m, player%2+1, board, ' ') == 0:
        print('No connect-M is possible for either player. The game is a tie.')
# end while (moves > 0)

printBoard(board) # show state of board at the end of the game
