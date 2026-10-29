
import chess
import time


board = chess.Board()

move = chess.Move.from_uci("e1g1")


white_pawns = board.pieces(chess.PAWN, chess.WHITE)
black_pawns = board.pieces(chess.PAWN, chess.BLACK)
white_king = board.pieces(chess.KING, chess.WHITE)
black_king = board.pieces(chess.KING, chess.BLACK)
white_knights = board.pieces(chess.KNIGHT, chess.WHITE)
black_knights = board.pieces(chess.KNIGHT, chess.BLACK)
black_bishops = board.pieces(chess.BISHOP, chess.BLACK)
white_bishops = board.pieces(chess.BISHOP, chess.WHITE)


def evaluate_board(board):
    if board.is_checkmate():
            # If it's checkmate, return a huge score
            if board.turn:  # White's turn to move, meaning Black delivered mate
                return -9999
            else:
                return 9999
        
    if board.is_stalemate() or board.is_insufficient_material():
            return 0
    
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    total_score = 0
    #so it STOP PLAYING A4 FOR THE 1000 TIME IN A ROW IT NEVER CAHNAGES 
    if chess.PAWN in white_pawns and chess.SQUARE_E4 in white_pawns:
        total_score += 0.5
    if chess.PAWN in white_pawns and chess.SQUARE_D4 in white_pawns:
        total_score += 0.5
    if chess.PAWN in black_pawns and chess.SQUARE_E5 in black_pawns:
        total_score -= 0.5
    if chess.PAWN in black_pawns and chess.SQUARE_D5 in black_pawns:
        total_score -= 0.5
    #if the chess enigne casles then more points 
    if board.is_castling(move):
        total_score += 0.5 if board.turn else -0.5


    #   I should use a list but that takes a lot of time
    if chess.KNIGHT in white_knights and chess.SQUARE_F3 in white_knights:
        total_score += 0.5
    if chess.KNIGHT in white_knights and chess.SQUARE_C3 in white_knights:
        total_score -= 0.5
    if chess.KNIGHT in black_knights and chess.SQUARE_F8 in black_knights:
        total_score += 0.5
    if chess.KNIGHT in black_knights and chess.SQUARE_C8 in black_knights:
        total_score -= 0.5
    if chess.KNIGHT in white_knights and chess.SQUARE_A3 in white_knights:  
        total_score -= 0.5
    if chess.KNIGHT in white_knights and chess.SQUARE_H3 in white_knights:  
            total_score -= 0.5
    if chess.KNIGHT in black_knights and chess.SQUARE_A6 in black_knights:
        total_score += 0.5
    if chess.KNIGHT in black_knights and chess.SQUARE_H6 in black_knights:
        total_score += 0.5
    #this is a tricky one for whichit shoukd be at
    if chess.BISHOP in white_bishops and chess.SQUARE_C4 in white_bishops:
        total_score += 0.2
    if chess.BISHOP in white_bishops and chess.SQUARE_F4 in white_bishops:
        total_score += 0.2
    if chess.BISHOP in black_bishops and chess.SQUARE_C5 in black_bishops:
        total_score -= 0.2
    if chess.BISHOP in black_bishops and chess.SQUARE_F5 in black_bishops:
        total_score -= 0.2
  

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = piece_values[piece.piece_type]
            # Add points if it's white, subtract if it's black
            if piece.color == chess.WHITE:
                total_score += value
            else:
                total_score -= value
                
    return total_score

    
def minimax(board, depth, maximizing_player):
     if depth == 0 or board.is_game_over():
        return evaluate_board(board)

     if maximizing_player:
        max_eval = float("-inf")
        #pushes every leagl move and the best one aka higest eval is done
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False)
            board.pop()  
            max_eval = max(max_eval, eval)
        return max_eval
     else:
        min_eval = float("inf")
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True)
            board.pop()  # Undo the move
            min_eval = min(min_eval, eval)
        return min_eval

def find_best_move(board, depth):
    best_move = None
    best_value = float("-inf") if board.turn else float("inf")

    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, not board.turn)
        board.pop()

        if (board.turn and board_value > best_value) or (not board.turn and board_value < best_value):
            best_value = board_value
            best_move = move

        elif not board.turn and board_value < best_value:
            best_value = board_value
            best_move = move

    return best_move


