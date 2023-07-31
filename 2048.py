import random
import os
import numpy as np

def pos__getAxisVector():
    pos = input('---->') ## getChar()
    if pos=='UP' or pos=='W' or pos=='w':
        pos = 'D2U'
    elif pos=='DOWN' or pos=='S' or pos=='s':
        pos = 'U2D'
    elif pos=='LEFT' or pos=='A' or pos=='a':
        pos = 'R2L'
    elif pos=='RIGHT' or pos=='D' or pos=='d':
        pos = 'L2R'
    return pos
def arr__getElementsAlongAxis(axis, cubic):
    global debug
    if debug:
        print('arr__getElementsAlongAxis')
        print(axis)
        [print(c) for c in cubic]
    if axis=='R2L':
        if debug:
            print('\treturn')
            [print('\t', c) for c in cubic]
        return cubic
    elif axis=='L2R':
        cubic = [c[::-1] for c in cubic]
        if debug:
            print('\treturn')
            [print('\t', c) for c in cubic]
        return cubic
    elif axis=='D2U':
        cubic = [[cubic[i][j] for i in range(len(cubic))] for j in range(len(cubic[0]))]
        if debug:
            print('\treturn')
            [print('\t', c) for c in cubic]
        return cubic
    elif axis=='U2D':
        cubic = [[cubic[-1-i][-1-j] for i in range(len(cubic))] for j in range(len(cubic[0]))]
        if debug:
            print('\treturn')
            [print('\t', c) for c in cubic]
        return cubic
    return cubic
def arr__combineAlongAxis(arr):
    global debug
    global score
    global adder
    if debug:
        print('arr__combineAlongAxis')
        [print(c) for c in cubic]
    N = len(arr)
    arr = [a for a in arr if a!=0]
    n = len(arr)
    i=0
    # print(arr)
    while i<n-1:
        if arr[i]==arr[i+1]:
            adder += arr[i+1]+arr[i]
            score += adder
            arr[i]+=arr[i+1]
            arr[i+1]=0
            i+=2
        else:
            i+=1
    arr = [a for a in arr if a!=0]
    arr = arr + [0] * (N-len(arr))
    return arr

def cubic__initBlocks(horizontalLim, verticalLim, initBlockNum):
    i = 0
    cubic = [[0 for i in range(horizontalLim)] for j in range(verticalLim)]
    return cubic__addBlocks(horizontalLim, verticalLim, initBlockNum, cubic)
def cubic__addBlocks(horizontalLim, verticalLim, addBlockNum, theCubic=None):
    global cubic
    if theCubic==None:
        theCubic = cubic
    i = 0
    while i<addBlockNum:
        x = random.randint(0, horizontalLim-1)
        y = random.randint(0, verticalLim-1)
        if theCubic[x][y] == 0:
            theCubic[x][y] = random.choice([2]*17+[4]*2+[8]*1)
            i+=1
    return theCubic
def canPlay(cubic):
    global horizontalLim
    global verticalLim
    flag = False
    for j in range(len(cubic)):
        for i in range(len(cubic[0])):
            for a,b in zip([1, -1, 1, -1], [0, 0, 1, 1]):
                if b==0:
                    x,y = i+a, j
                else:
                    x,y = i, j+a
                if 0<=x and x<horizontalLim and 0<=y and y<verticalLim:
                    if debug:
                        print(x, y, end='')
                        print(cubic[y][x])
                        print(i, j, end='')
                        print(cubic[j][i], '\n\n')
                    if cubic[y][x]==cubic[j][i] or (cubic[y][x]==0 or cubic[j][i]==0):
                        flag = True
                        break
    return flag
def str__scriptedNum(num, max_len):
    num_len = int(np.log(10, num))
    return ' '*int(max_len-int(max_len/2))+str(num)+' '*int(max_len/2)
def easy_updatePixel(cubic):
    global debug
    global score
    global adder
    global round_
    if not debug:
        os.system('cls')
    if round_==0:
        print('==== START NEW GAME ====')
    if round_<0:
        print('==== RESUME OLD GAME ====')
        round_ = -round_
    [print(c) for c in cubic]
    if adder==0:
        print('\nScore: %d'%score)
    else:
        print('\nScore: %d(+%d)'%(score, adder))
    print('Move: %d'%(round_))
    adder = 0
    return round_+1 if round_!=-1 else -1
def updatePixel(cubic):
    global horizontalLim
    global verticalLim
    max_ = 0
    max_len = int(np.log10([max([max(c) for c in cubic])])[0])
    print_flag = False
    # os.system('cls')
    ## frame
    print('■'*int(2+horizontalLim*(2*2/2+1*2/2+max_len//2)))
    for ti in range(verticalLim):
        for ivv in range(max_len):
            print('■',end='')
            for it in range(horizontalLim):
                if int(max_len/2)<ivv:# and not flag:
                    print_flag=True
                    num = cubic[it][ti]
                    print(' '*2+'%s'%str__scriptedNum(num, max_len)+' '*2+'■')
                else:
                    ## upper/lower space
                    for i in range(horizontalLim):
                        print(' '*int(2*2+max_len)+'■', end='')
                    print('', end='')
                print(' '*int(2*2+max_len)+'■', end='')
    ## frame
    print('■'*int(2+horizontalLim*(2*2/2+1*2/2+max_len//2)))
    ## next step
    print('\n\n\n\nNext Instrctor')
def cubic__setInitState():
    global horizontalLim
    global verticalLim
    print('Input The Number And Seperate With Space, \'SPACE\' or \'0\' PLEASE TYPE \'0\', \'LAST\' For The Leaving...')
    cubic = []
    text = input('---->')
    while text!='LAST':
        if text!='':
            cubic.append([int(t) for t in text.split(' ')])
        else:
            cubic.append([])
        text = input('---->')
    max_len = max([max(c) for c in cubic])
    for line in cubic:
        if len(line)<max_len:
            line = line + [0]*(max_len-len(line))
    horizontalLim = len(cubic[0])
    verticalLim = len(cubic)
    if debug:
        print(horizontalLim, verticalLim)
    return cubic
# 1024 0 0 4096
# 512 256 128 0
# 16 8 4 2
# 2 2 2 2
# LAST
def getCubicScore():
    global cubic
    global score
    global round_
    numbers = []
    extract_ = [[cubic[i][j] for i in range(len(cubic)) if cubic[i][j]!=0] for j in range(len(cubic[0]))]
    for e in extract_:
        numbers += e if e!=[] else []
    if debug=='cubicScore':
        print(numbers)
    for n,e in zip(numbers, np.log2(numbers)):
        if debug=='cubicScore':
            print(n, e, n*(e-1), 2**(e-1)-1)
        print(n, e, n*(e-1), 2**(e-1)-1)
        score+=n*(e-1)
        round_+=e
    return score, round_

debug = False
horizontalLim, verticalLim = 4, 4
initBlockNum = random.randint(1,3)
mode = input('Play New Game (N) / Play Specific Game (S) / Exit (E)\nInput The Mode You Want ----->')
cubic = None
score = 0
adder = 0
round_ = 0
if mode=='N':
    cubic = cubic__initBlocks(horizontalLim, verticalLim, initBlockNum)
elif mode=='S':
    cubic = cubic__setInitState()
    score, round_ = getCubicScore()
elif mode=='E':
    exit()
new_cubic = None
while canPlay(cubic):
    # updatePixel(cubic)
    round_ = easy_updatePixel(cubic)
    axis = pos__getAxisVector()
    # cubic = arr__getElementsAlongAxis(axis, [arr__combineAlongAxis(c) for c in arr__getElementsAlongAxis(axis, cubic)])
    new_cubic = [arr__combineAlongAxis(c) for c in arr__getElementsAlongAxis(axis, cubic)]
    if debug:
        [print(c) for c in new_cubic]
    new_cubic = arr__getElementsAlongAxis(axis, new_cubic)
    if cubic!=new_cubic:
        cubic = new_cubic
        cubic = cubic__addBlocks(horizontalLim, verticalLim, 1)
    else:
        adder = 0
        round_ -= 1
    if debug:
        [print(c) for c in new_cubic]
print('==== GAME OVER ====')


