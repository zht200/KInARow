def introduce():
  return "I am the Prince Charming. I like playing chess and always trying to be a gentleman. I was created by Zhitan Zhang(zhitan) and Xiao Tan(xt64). "

def nickname():
  return "Prince Charming"

import random
def prepare(initial_state, k, what_side_I_play, opponent_nickname):
  global K, MY_SIDE_LETTER, NUM_ROWS, NUM_COLUMNS, POSSIBLE_WIN_LIST, SCORE_HASH, ZOBRIST_NUM, OPPONENT_NICKNAME
  K = k
  MY_SIDE_LETTER = what_side_I_play
  NUM_ROWS = len(initial_state[0])
  NUM_COLUMNS = len(initial_state[0][0])
  if K < 2 or K>NUM_COLUMNS or K >NUM_ROWS:
    print("Invalid K.")
    return
  POSSIBLE_WIN_LIST = [] # has the form [[(0,0),(0,1),(0,2),...], [(1,2),(2,3),(3,4),...], ...]
  for row in range(NUM_ROWS):
    for column in range(NUM_COLUMNS):
      if row+K <= NUM_ROWS: # in a column
        temp = []
        for i in range(row, row+K):
          if initial_state[0][i][column] == '-':
            break; # does not count forbidden squares
          temp.append((i, column))
        if len(temp) == K: # no forbidden squares
          POSSIBLE_WIN_LIST.append(temp)
      if column+K <= NUM_COLUMNS: # in a row
        temp = []
        for i in range(column, column+K):
          if initial_state[0][row][i] == '-':
            break; # does not count forbidden squares
          temp.append((row, i))
        if len(temp) == K: # no forbidden squares
          POSSIBLE_WIN_LIST.append(temp)
      if column+K <= NUM_COLUMNS and row+K <= NUM_ROWS: # right-down diagonal
        temp = []
        j = column
        for i in range(row, row+K):
          if initial_state[0][i][j] == '-':
            break;
          temp.append((i, j))
          j += 1
        if len(temp) == K: # no forbidden squares
          POSSIBLE_WIN_LIST.append(temp)
      if column+K <= NUM_COLUMNS and row-K >= -1: # right-up diagonal
        temp = []
        j = column
        for i in range(row,row-K,-1):
          if initial_state[0][i][j] == '-':
            break;
          temp.append((i, j))
          j += 1
        if len(temp) == K: # no forbidden squares
          POSSIBLE_WIN_LIST.append(temp)
  SCORE_HASH = {} # key is the Zobrist hash key (integer) for a board, value is corresponding score
  ZOBRIST_NUM = [] # [[[value for X, value for O],[value for X, value for O],...],[second row...],...]
  for row in range(NUM_ROWS):
    temp1 = []
    for column in range(NUM_COLUMNS):
      temp2 = [] # most inner one, values for X, O
      temp2.append(random.randint(0,4294967296)) # for X
      temp2.append(random.randint(0,4294967296)) # for O
      temp1.append(temp2)
    ZOBRIST_NUM.append(temp1)
  OPPONENT_NICKNAME = opponent_nickname

import time
def makeMove(currentState, currentRemark, timeLimit=10000):
  start_time = time.time()
  [newState,score] = minimax_with_alpha_beta(currentState, 4, -999999999, 999999999, timeLimit, start_time, None)
  # score can be used to determine the remark
  newRemark = response(score, currentRemark)
  (a,b)=(-1,-1)
  # find the position of the move
  for row in range(NUM_ROWS):
    for column in range(NUM_COLUMNS):
      if not currentState[0][row][column] == newState[0][row][column]:
        (a,b)=(row,column)
  if (a,b) == (-1,-1):
    return [None, "A friendly game! I like it."] # all squares are filled
  return [[(a,b), newState], newRemark]

def response(score, currentRemark):
    global OPPONENT_NICKNAME
    if MY_SIDE_LETTER != "X": score = score * (-1)
    print(score)
    newremark = ""
    if score >= -1000 and score <-500:
        newremark = "You are in a good situation, " + OPPONENT_NICKNAME + "! Guess what I am going to do."
    if score >= -2000 and score <-1000:
        newremark = "Oh " + OPPONENT_NICKNAME + ", I think you are going to beat me this time!"
    if score <-2000:
        newremark = "You deserve the victory. I appreciate your intelligence " + OPPONENT_NICKNAME + "! Let's play again."
    if score >= 500 and score < 1000:
        newremark = "It becomes harder for you. I wish you could still enjoy it. Do you need my help?"
    if score >=1000 and score < 2000:
        newremark = OPPONENT_NICKNAME + ", I guess I am going to win the game if you do not pay more attention on it!"
    if score >=2000:
        newremark = "I am sorry but it seems that I will win the game. Thank you for your time " + OPPONENT_NICKNAME + "!"
    if newremark != "": return newremark
    if "win" in currentRemark:
        newremark = "It is too early to say the word 'win', " + OPPONENT_NICKNAME + "!"
        return newremark
    if "beat" in currentRemark and "you" in currentRemark:
        newremark = "Please do not be so rude " + OPPONENT_NICKNAME + ". We are playing a game."
        return newremark
    if "best" in currentRemark:
        newremark = "Everyone wants to be the best. I admire your ambition."
        return newremark
    if "you" in currentRemark or "You" in currentRemark:
        newremark = "I don't think so."
        return newremark
    if "lose" in currentRemark:
        newremark = "Believe me, nobody will lose if he/she tries the best."
        return newremark
    if score >= -10 and score < 10:
        newremark = "The royal life is so boring. I feel happy to play game with you, " + OPPONENT_NICKNAME + "!"
    if score >= 10 and score < 50:
        newremark = "I will try to be a gentleman in this game."
    if score >= 50 and score < 200:
        newremark = "I am feeling good in playing this game. Could you come to my Palace every day?"
    if score >= 200 and score < 500:
        newremark = "Be careful! I do not want you to feel bad when playing with me, " + OPPONENT_NICKNAME + "!"
    if score >=-50 and score < -10:
        newremark = "You know, I am not a tough person. " + OPPONENT_NICKNAME + ", take it easy."
    if score >=-200 and score < -50:
        newremark = "The weather is so good today. But I am not in the mood for playing the game."
    if score >=-500 and score <-200:
        newremark = "I think you are a good player, " + OPPONENT_NICKNAME + ". I need to pay more attention on the game."
    return newremark

# Beta is the minimum upper bound of possible solutions
# Alpha is the maximum lower bound of possible solutions
# State[0][][] stores the board. State[1] stores X or O. State[2] stores hash value of itself
import copy
def minimax_with_alpha_beta(currentState, depth, alpha, beta, timeLimit, start_time, hashKey):
  if hashKey == None:
    hashKey = getHashKey(currentState[0])
  global SCORE_HASH
  if hashKey in SCORE_HASH: # determine if it's already been evaluated
    currentScore = SCORE_HASH[hashKey]
  else:
    currentScore = staticEval(currentState)
    SCORE_HASH[hashKey] = currentScore
  if (time.time() - start_time > timeLimit - 0.1) or (depth == 0): # 0.1 second from time limit, arbitrary, may need to change other number
    return [currentState,currentScore]
  global NUM_ROWS, NUM_COLUMNS, ZOBRIST_NUM
  # find list of available moves
  available_moves = []
  for row in range(NUM_ROWS):
    for column in range(NUM_COLUMNS):
      if currentState[0][row][column] == ' ':
        temp = []
        temp.append(copy.deepcopy(currentState[0]))
        temp[0][row][column] = currentState[1]
        if currentState[1] == 'X':
          temp.append('O')
          temp.append(currentScore ^ ZOBRIST_NUM[row][column][0]) # append Zobrist hash key
        else:
          temp.append('X')
          temp.append(currentScore ^ ZOBRIST_NUM[row][column][1]) # append Zobrist hash key
        available_moves.append(temp)
  if len(available_moves) == 0:
    return [currentState,currentScore]
  if currentState[1] == 'X': # select maximum children
    v = alpha
    newState = currentState
    for available_state in available_moves:
      [tempState,tempScore] = minimax_with_alpha_beta(available_state[0:2],depth-1,v,beta,timeLimit,start_time,available_state[2])
      if tempScore > v: # greater than previous maximum lower bound 
        v = tempScore
        newState = available_state[0:2]
      if v >= beta: # greater than or equal to upper bound
        break
    return [newState,v]
  else: # select minimum children
    v = beta
    newState = currentState
    for available_state in available_moves:
      [tempState,tempScore] = minimax_with_alpha_beta(available_state[0:2],depth-1,alpha,v,timeLimit,start_time,available_state[2])
      if tempScore < v: # smaller than previous maximum upper bound 
        v = tempScore
        newState = available_state[0:2]
      if v <= alpha: # smaller than or equal to lower bound
        break
    return [newState,v]

def getHashKey(board):
  global NUM_ROWS, NUM_COLUMNS, ZOBRIST_NUM
  val = 0
  for row in range(NUM_ROWS):
    for column in range(NUM_COLUMNS):
      piece = None
      if (board[row][column] == "X"):
        piece = 0
      if (board[row][column] == "O"):
        piece = 1
      if (piece != None):
        val = val ^ ZOBRIST_NUM[row][column][piece]
  return val

def staticEval(state):
  win_list = [] # has the form [[X,X,O, ,...],[O,X,O,...],...]
  global POSSIBLE_WIN_LIST
  for win_combination in POSSIBLE_WIN_LIST:
    temp = []
    for (a,b) in win_combination:
      temp.append(state[0][a][b])
    win_list.append(temp)
  score = 0
  global K
  for win_combination in win_list:
    x_num = win_combination.count('X')
    if x_num > 0:
      first_x_index = win_combination.index('X')
    o_num = win_combination.count('O')
    if o_num > 0:
      first_o_index = win_combination.index('O')
    if x_num > 0:
      if x_num == K: # K of X's
        score += 10000
      if x_num == K-1 and o_num == 0: # K-1 of X's, no O
        score += 1000
      if x_num == K-2 and o_num == 0: # K-2 of X's, no O
        score += 100
      if x_num == 2 and win_combination[first_x_index+1] == 'X' and o_num == 0: # 2 consecutive X's, no O
        score += 10
      if x_num == 1 and o_num == 0:
        score += 1
    if o_num > 0:
      if o_num == K: # K of O's
        score -= 10000
      if o_num == K-1 and x_num == 0: # K-1 of O's, no X
        score -= 1000
      if o_num == K-2 and x_num == 0: # K-2 of O's, no X
        score -= 100
      if o_num == 2 and win_combination[first_o_index+1] == 'O' and x_num == 0: # 2 consecutive O's, no X
        score -= 10
      if o_num == 1 and x_num == 0:
        score -= 1
  return score

