# ----------------------------------------------------------------------------------
def linha_zerada(vetor):
   for element in vetor:
       if element !=0:
           return False      
   return True 
       
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

lista = [1,1,1,0]
x = submatriz(lista)

print("Avaliação:",x)