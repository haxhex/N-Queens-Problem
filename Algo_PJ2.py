"""
Author : Helia Ghorbani
Student ID : 9824353
"""
import pygame

pygame.init()

# declare window size parameters : height, width
winSize = 100
height = winSize * 6
width = height + winSize * 2
# ---------------------------------------------------------
board = []
btnOffset = (winSize * 2) // 3
run = True
pressed = False
number = ''
N = 0
page = 0
isSolved = False
# ---------------------------------------------------------
# colors
BLACK  = (0,0,0)
LIGHTGRAY = (211,211,211)
RED = (255, 0, 0)
TURQUOISE = (64,224,208)
LIGHTCORAL = (240,128,128)
# ---------------------------------------------------------
# set display window size : height, width 
window = pygame.display.set_mode((width,height))
pygame.display.set_caption('N-Queens Problem')
# ---------------------------------------------------------
# set display font
titleFont = pygame.font.SysFont('Helvetica', 30, bold=True)
textFont = pygame.font.SysFont('Helvetica', 20, bold=True)
# ---------------------------------------------------------
# set solve button 
solveBtn = pygame.Rect(0,0, 100, 50)
solveBtn.center = (width // 2, height // 2 + height // 6)
# ---------------------------------------------------------
# Set previous, next and clear button
prvBtn = pygame.Rect(0, 0, 75, 50)
nxtBtn = pygame.Rect(0, 0, 75, 50)
prvBtn.center = (height + btnOffset - 10, 100)
nxtBtn.center = (height + btnOffset * 2 + 10 ,100)
clrBtn = pygame.Rect(0, 0, 75, 50)
clrBtn.center = (height + (width - height) // 2, height // 2)
# ---------------------------------------------------------
# check left diagonal
def checkLeftDiagonal(arr, row, col):
    x = y = 0
    if row > col:
        x = row - col
        y = 0
    elif col > row:
        x = 0
        y = col - row
    while ((x != len(arr)) and (y != len(arr[0]))):
        if arr[x][y] == 1:
            return False
        x = x + 1
        y = y + 1
    return True
# ---------------------------------------------------------
# check right digonal
def checkRightDiagonal(arr, row, col):
    x = row
    y = col
    while x != 0 and y != len(arr) - 1:
        x = x - 1
        y = y + 1
    while x != len(arr) and y >= 0:
        if arr[x][y] == 1:
            return False
        x = x + 1
        y = y - 1
    return True
# ---------------------------------------------------------
# check vlidation of movement
# check row, column, diagonal
# 1 means full -> False
def validMove(arr, row, col):
    # check row - no other 1 in row
    for i in range(len(arr[0])):
        if arr[row][i]:
            return False
    # check column - no other 1 in column
    for i in range(len(arr[col])):  
        if arr[i][col]:
            return False
    # check right and left digonal
    if not (checkRightDiagonal(arr, row, col) and checkLeftDiagonal(arr, row, col)):
        return False
    return True
# ---------------------------------------------------------
# return a copy of input array
def copyArray(arr,N):
    array = initArray(N)
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            array[i][j] = arr[i][j]
    return array
# ---------------------------------------------------------
# find suitable place
# solve recursuvely
def NQueensSolver(arr, col):
    global board
    result = False
    # return true if all queens placed
    if col >= len(arr[0]) :
        board.append(copyArray(arr, len(arr)))
        return True
    # consider this column and place this in all row
    for row in range(len(arr[0])):
        # check can be placed in arr[row][col]
        if validMove(arr, row, col):
            # placed in arr[row][col]
            arr[row][col] = 1
            # possible placement
            result = NQueensSolver(arr, col + 1) or result
            # placing in arr[row][col] doesn't lead to solution
            # remove from arr[row][col]
            # backtrack
            arr[row][col] = 0
    # if can't place in any row false
    return result
# ---------------------------------------------------------
# draw chessboard
def chessboard(N):
    cellSize = height // N
    # set black cells
    for i in range(N):
        for j in range(N):
            if i % 2 == 0 and j % 2 != 0:
                pygame.draw.rect(window, BLACK, (cellSize * i, cellSize * j, cellSize,cellSize ))
            elif i % 2 != 0 and j % 2 == 0:
                pygame.draw.rect(window, BLACK, (cellSize * i, cellSize * j , cellSize, cellSize))
    # draw lines around the board
    pygame.draw.line(window, BLACK, (0, 0), (cellSize * N, 0))
    pygame.draw.line(window,BLACK,(cellSize * N, 0),(cellSize * N, cellSize * N))
# ---------------------------------------------------------
# number of solution
def numOfSol(page, arr):
    # display page number
    string = '{} / {}'
    pageNum = textFont.render(string.format(str(page + 1), str(len(arr))), 1, BLACK)
    # set position of page number
    pagenumRect = pageNum.get_rect()
    pagenumRect.center = (height + (width - height) // 2, 50)
    window.blit(pageNum, pagenumRect)
    # draw pervious, next and clear button on the board
    pygame.draw.rect(window, TURQUOISE, prvBtn)
    pygame.draw.rect(window, TURQUOISE, nxtBtn)
    pygame.draw.rect(window, LIGHTCORAL, clrBtn)
    # set text and position of pervious button
    prv = textFont.render('Previous', 1, BLACK)
    prvRect = prv.get_rect()
    prvRect.center = prvBtn.center
    window.blit(prv, prvRect)
    # set text and position of next button
    nxt = textFont.render('Next', 1, BLACK)
    nxtRect = nxt.get_rect()
    nxtRect.center = nxtBtn.center
    window.blit(nxt, nxtRect)
    # set text and position of clear button
    clear = textFont.render('Clear', 1, BLACK)
    clearRect = clear.get_rect()
    clearRect.center = clrBtn.center
    window.blit(clear, clearRect)
# ---------------------------------------------------------
# fill cell -> put red rect on selected cell
def fillCell(arr, N):
    cellSize = height // N
    queenSize = cellSize // 1.5
    queenOffset = (cellSize - queenSize) // 2
    for row in range(len(arr)):
        for col in range(len(arr[0])):
            if arr[row][col]:
                pygame.draw.rect(window, RED, (col * cellSize + queenOffset, row * cellSize + queenOffset, queenSize, queenSize))
# ---------------------------------------------------------
# make empty N x N matrix 
def initArray(N):
    return [[0 for i in range(N)] for j in range(N)]
# ---------------------------------------------------------
# first page - text & button display
def menu():
    # first page - text, position
    text = titleFont.render("Enter number of Queens (at least 4)",1 ,BLACK)
    textRect = text.get_rect()
    textRect.center = (width //2 , height // 2 - height // 6)
    window.blit(text, textRect)
    # draw solve button
    pygame.draw.rect(window, TURQUOISE, solveBtn)
    # set text and position of solve button
    solve = titleFont.render('Solve', 1, BLACK)
    solveTextRect = solve.get_rect()
    solveTextRect.center = (width // 2, height // 2 + height // 6)
    window.blit(solve, solveTextRect)
# ---------------------------------------------------------
# display input number of queens
def num(number):
    # set text and position of number of queens
    inputNum = titleFont.render(number, 1, BLACK)
    inputNumRect = inputNum.get_rect()
    inputNumRect.center = (width //2 , height // 2)
    window.blit(inputNum, inputNumRect)
# ---------------------------------------------------------
# main func
def main():
    global run, pressed, number, isSolved, board, page
    while run:
        # set window background
        window.fill(LIGHTGRAY)
        # no answer for N = 2 & N = 3
        if not pressed or N == 2 or N == 3:
            # display first page
            menu()
            # display input number
            num(number)
            # input is accepted (not 2 or 3)
            pressed = False
        elif N > 3 or N == 1:
            # init N x N empty array
            array = initArray(N)
            # draw N x N chessboard
            chessboard(N)
            # check if solved
            # prevent solving everytime after changing page
            if isSolved:
                NQueensSolver(array, 0)
                isSolved = False
            # fill selected position
            fillCell(board[page], N)
            # display number of solution
            numOfSol(page, board)
        # events : press a key, click
        for event in pygame.event.get():
            # event - press key
            if event.type == pygame.KEYDOWN:
                # press a number
                if event.unicode.isdigit():
                    number += event.unicode
                # press backspace or del
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    number = number[:-1]
            # mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]
                # click on solve button
                if solveBtn.collidepoint(x, y) and not pressed:
                    if number != '':
                        N = int(number)
                        number = ''
                        pressed = True
                        isSolved  = True
                # click on prevoius button
                elif prvBtn.collidepoint(x, y) and page > 0:
                    page = page - 1
                # click on next button
                elif nxtBtn.collidepoint(x, y) and page < len(board) - 1:
                    page = page + 1
                # click on clear button - start again
                elif clrBtn.collidepoint(x, y):
                    pressed = False
                    isSolved = False
                    board = []
                    page = 0
            # terminate - close
            elif event.type == pygame.QUIT:
                run = False
        # upadate display
        pygame.display.update()
# ---------------------------------------------------------
# driver
if __name__ == '__main__':
    main()
    pygame.quit()