"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    Simulates a trial of Tic-Tac-Toe. Two players
    take turns to choose a randomly selected non-empty
    square until one wins.
    """
    while board.check_win() == None:
        empty_square = random.choice(board.get_empty_squares())
        row = empty_square[0]
        col = empty_square[1]
        board.move(row, col, player)
        if board.check_win() != None:
            return
        player = provided.switch_player(player)
        

def mc_update_scores(scores, board, player):
     """
     Takes a grid of scores (a list of lists) with the same 
     dimensions as the Tic-Tac-Toe board, a board from a completed game, 
     and which player the machine player is. It scores the 
     completed board and updates the scores grid. 
    """
    current_player = player
    other_player = provided.switch_player(player)
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):  
            if board.check_win() == current_player and board.square(row,col) == current_player:
                scores[row][col] += SCORE_CURRENT
            elif board.check_win() == current_player and board.square(row,col) == other_player:
                scores[row][col] -= SCORE_OTHER
            elif board.check_win() == other_player and board.square(row, col) == other_player:
                scores[row][col] += SCORE_OTHER
            elif board.check_win() == other_player and board.square(row,col) == current_player:
                scores[row][col] -= SCORE_CURRENT
            
def get_best_move(board, scores):
    """
    Takes a current board and a grid of scores, find all
    of the empty squares with the maximum score and randomly
    return one of them as a (row, colum) tuple.
    """
    score_values =[]
    score_dict = {}
    empty_squares = board.get_empty_squares()
    max_score_squares = [] 
    if len(empty_squares) == 0:
        return 
    for row, col in empty_squares:
        score = scores[row][col]
        score_values.append(score)
        score_dict[(row, col)] = score
    max_score = max(score_values)
    for key, value in score_dict.items():
        if value == max_score:
            max_score_squares.append(key)            
    return random.choice(max_score_squares)

def mc_move(board, player, trials):
    """
    Use the Monte Carlo simulation to return a move
    for the machine player in the form of a (row, col)
    tuple.
    """
    scores = [[0 for dummy_row in range(board.get_dim())]
              for dummy_col in range(board.get_dim())]
    for dummy in range(trials):
        clone_board = board.clone()
        mc_trial(clone_board, player)
        mc_update_scores(scores, clone_board, player)
    return get_best_move(board, scores)


 provided.play_game(mc_move, NTRIALS, False)        
 poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

