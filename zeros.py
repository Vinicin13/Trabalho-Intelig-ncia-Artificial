import numpy as np
import time 
from os import system, name

ROWS = 9
COLUMNS = 10
profundidade_heuristica=4
profundidade_minimax=4
global_variable = 0


# ----------------------------------------------------------------------------------
def clear():
    # para windows
    if name == 'nt':
        _ = system('cls')

    # para mac e linux(aqui, os.name eh 'posix')
    else:
        _ = system('clear')

# ----------------------------------------------------------------------------------
def create_board():
    board = np.zeros((ROWS, COLUMNS))
    return board

# ----------------------------------------------------------------------------------
def valid_location(board, column):
    return board[ROWS - 1][column] == 0

# ----------------------------------------------------------------------------------
def drop_piece(board, column, piece):
    for r in range(ROWS):
        if board[r][column] == 0:
            board[r][column] = piece
            return

# ----------------------------------------------------------------------------------
def is_winning_move(board, piece):
    # verifica se existem quatro peças em linha na horizontal, vertical e diagonais
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True

# ----------------------------------------------------------------------------------
def linha_zerada(vetor):
   for element in vetor:
       if element !=0:
           return False      
   return True 
       
# ----------------------------------------------------------------------------------
def heuristica(board):
    avaliacao = 0
    global global_variable

    for row in range(len(board)):
        for col in range(len(board[row])-profundidade_heuristica):
            window = board[row][col:col+profundidade_heuristica]
            global_variable = global_variable + 1 
            if linha_zerada(window):
                break
            avaliacao += submatriz(window)

    for col in range(len(board[0])):
        for row in range(len(board)-profundidade_heuristica):
            window = [board[row+i][col] for i in range(profundidade_heuristica)]
            global_variable = global_variable + 1
            avaliacao += submatriz(window)

    for row in range(len(board)-profundidade_heuristica):
        for col in range(len(board[row])-profundidade_heuristica):
            window = [board[row+i][col+i] for i in range(profundidade_heuristica)]
            global_variable = global_variable + 1
            avaliacao += submatriz(window)

    for row in range(len(board)-profundidade_heuristica):
        for col in range(len(board[row])-profundidade_heuristica):
            window = [board[row+i][col+profundidade_heuristica-i] for i in range(profundidade_heuristica)]
            global_variable = global_variable + 1
            avaliacao += submatriz(window)
    return avaliacao
# ----------------------------------------------------------------------------------
def submatriz(window):
    avaliacao = 0
    player_pieces = 0
    opponent_pieces = 0
    empty_pieces = 0
   
    if linha_zerada(window):
        return avaliacao
    
    for piece in window:
        if piece == 2:
            player_pieces += 1
        elif piece == 1:
            opponent_pieces += 1
        elif piece == 0:
            empty_pieces += 1

    if player_pieces == 4:
        avaliacao += 100
    elif player_pieces == 3 and opponent_pieces == 0:
        avaliacao += 75
    elif player_pieces == 2 and opponent_pieces == 0:
        avaliacao += 50
    elif opponent_pieces == 3 and player_pieces == 0:
        avaliacao -= 75

    return avaliacao
# ----------------------------------------------------------------------------------
def minimax(board, depth, maximizing_player):
    if is_winning_move(board, 2):  # IA ganhou
        return (None, 100)
    elif is_winning_move(board, 1):  # jogador humano ganhou
        return (None, -100)
    elif len(get_valid_locations(board)) == 0:  # jogo empatado
        return (None, heuristica(board))
    elif depth == 0:  # profundidade máxima atingida
        return (None, heuristica(board))

    valid_locations = get_valid_locations(board)
    if maximizing_player:
        value = -np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            temp_board = board.copy()
            drop_piece(temp_board, col, 2)
            new_score = minimax(temp_board, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value

    else:  # minimizing player
        value = np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            temp_board = board.copy()
            drop_piece(temp_board, col, 1)
            new_score = minimax(temp_board, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value

# ----------------------------------------------------------------------------------
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMNS):
        if valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


# ----------------------------------------------------------------------------------
# CSI457 
# Programa Principal
# Data: 13/07/2023
# Autores: Daniel Rodrigues Martins, Stephane Matos Oliveira, Vinicius Gabriel Albuquerque
# ----------------------------------------------------------------------------------
board = create_board()
game_over = False
turn = 0

clear()
while not game_over:
    # Movimento do Jogador 1
    if turn == 0:
        col = int(input("Jogador 1, selecione a coluna (0-9):"))
        if valid_location(board, col):
            drop_piece(board, col, 1)
            if is_winning_move(board, 1):
                print("Jogador 1 Vence!! Parabéns!!")
                game_over = True

    # Movimento da IA
    else:
        t1 = time.time()
        col, minimax_score = minimax(board, profundidade_minimax, True)
        if valid_location(board, col):
            drop_piece(board, col, 2)
            if is_winning_move(board, 2):
                print("Jogador 2 Vence!!!")
                game_over = True
        t2 = time.time()
        tempo_execucao = t2 - t1 
        print("Tempo de Execução: ", tempo_execucao)        

    print("Quantidade de estados visitados:",global_variable)
    print(board)
    print(" ")
    turn += 1
    turn = turn % 2