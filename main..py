import numpy as np
import chess
import time


board = chess.Board()
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

        if (board.turn and board_value > best_value) | (not board.turn and board_value < best_value):
            best_value = board_value
            best_move = move

        elif not board.turn & board_value < best_value:
            best_value = board_value
            best_move = move

    return best_move


