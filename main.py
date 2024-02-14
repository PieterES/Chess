import copy
import sys
from copy import deepcopy
import pygame

# Initialize Pygame
pygame.init()

# Constants
messagebox_width, messagebox_height = 200, 100
BUTTON_COLOUR = (100, 100, 100)
WIDTH, HEIGHT = 400, 400
SQAURE_SIZE = WIDTH // 8
BLACK = (101, 67, 33)
WHITE = (219, 182, 122)
SELECTED_COLOUR = (0, 255, 0)
LEGAL_MOVE_COLOR = (169, 169, 169)
PIECE_SIZE = (47.5, 47.5)

# Promotion screen
promotion_width, promotion_height = 300, 150
promotion_screen = pygame.Surface((promotion_width, promotion_height))
promotion_screen.fill((255, 255, 255))
promotion_screen_rect = promotion_screen.get_rect(center=(WIDTH//2, HEIGHT//2))
# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

images = {
    'P': pygame.transform.scale(pygame.image.load('images/Chess_plt45.png'), PIECE_SIZE),
    'R': pygame.transform.scale(pygame.image.load('images/Chess_rlt45.png'), PIECE_SIZE),
    'N': pygame.transform.scale(pygame.image.load('images/Chess_nlt45.png'), PIECE_SIZE),
    'B': pygame.transform.scale(pygame.image.load('images/Chess_blt45.png'), PIECE_SIZE),
    'Q': pygame.transform.scale(pygame.image.load('images/Chess_qlt45.png'), PIECE_SIZE),
    'K': pygame.transform.scale(pygame.image.load('images/Chess_klt45.png'), PIECE_SIZE),
    'p': pygame.transform.scale(pygame.image.load('images/Chess_pdt45.png'), PIECE_SIZE),
    'r': pygame.transform.scale(pygame.image.load('images/Chess_rdt45.png'), PIECE_SIZE),
    'n': pygame.transform.scale(pygame.image.load('images/Chess_ndt45.png'), PIECE_SIZE),
    'b': pygame.transform.scale(pygame.image.load('images/Chess_bdt45.png'), PIECE_SIZE),
    'q': pygame.transform.scale(pygame.image.load('images/Chess_qdt45.png'), PIECE_SIZE),
    'k': pygame.transform.scale(pygame.image.load('images/Chess_kdt45.png'), PIECE_SIZE),
}

# Chessboard
colors = [WHITE, BLACK]
message = None
font = pygame.font.Font(None, 36)
chessboard = [[colors[(i+j) % 2] for j in range(8)] for i in range(8)]

# Current player's turn (1 for white, -1 for black)
current_turn = 1

# Pieces
pieces = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ["p"] * 8,
    [""] * 8,
    [""] * 8,
    [""] * 8,
    [""] * 8,
    ["P"] * 8,
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
]


# Selected
selected_piece = None
selected_position = None
legal_moves = None
last_move = None
last_moved_piece = None
attack_moves = None
en_passant_target = None
white_king_moved = False
black_king_moved = False
lwr_moved = False
rwr_moved = False
lbr_moved = False
rbr_moved = False
white_king_pos = (7, 4)
black_king_pos = (0, 4)
WIDTH, HEIGHT = 400, 200
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.Font(None, 36)
# turn 1 = white = upper
# turn -1 = black = lower

def reset_game():
    global pieces, current_turn, selected_piece, selected_position, legal_moves, last_move, last_moved_piece, en_passant_target, attack_moves, message
    global white_king_pos, black_king_pos, white_king_moved, black_king_moved, lwr_moved, rwr_moved, lbr_moved, rbr_moved

    # Reset chessboard
    pieces = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ["p"] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        ["P"] * 8,
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ]

    # Reset other game-related variables
    current_turn = 1
    selected_piece = None
    selected_position = None
    legal_moves = None
    last_move = None
    last_moved_piece = None
    en_passant_target = None
    attack_moves = None
    white_king_pos = (7, 4)
    black_king_pos = (0, 4)
    message = None
    draw_chessboard(screen, chessboard, pieces, legal_moves, message)

# Function to draw a button
def draw_button(x, y, width, height, text, hover=False):
    button_color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, (x, y, width, height))

    text_surface = FONT.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)
    return text_rect
def draw_message_box(message):
    pygame.draw.rect(screen, (200, 200, 200), (50, 25, 300, 150))

    # Draw message text
    message_text = FONT.render(message, True, (0, 0, 0))
    message_rect = message_text.get_rect(center=(WIDTH / 2, 50))
    screen.blit(message_text, message_rect)
    # Draw message text
    if message == 'Checkmate!':
        if current_turn == 1:
            message_text = FONT.render('Black Wins!', True, (0, 0, 0))
            message_rect = message_text.get_rect(center=(WIDTH / 2, 75))
            screen.blit(message_text, message_rect)
        if current_turn == -1:
            message_text = FONT.render('White Wins!', True, (0, 0, 0))
            message_rect = message_text.get_rect(center=(WIDTH / 2, 75))
            screen.blit(message_text, message_rect)
    # Draw buttons
    reset_button_rect = draw_button(75, 100, BUTTON_WIDTH, BUTTON_HEIGHT, "Reset")
    quit_button_rect = draw_button(225, 100, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit")
    return quit_button_rect, reset_button_rect
def show_message_box(message):
    quit_button_rect, reset_button_rect = draw_message_box(message)

    pygame.display.flip()

    while message:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if reset_button_rect.collidepoint(event.pos):
                    reset_game()
                    message = None

def attacks_opponent(pieces, current_turn):
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    all_moves_for_check = []
    for row in range(8):
        for col in range(8):
            piece = pieces[row][col]
            if current_turn == 1:
                if piece == 'n':
                    for move in knight_moves:
                        new_row, new_col = row + move[0], col + move[1]
                        if 0 <= new_row < 8 and 0 <= new_col < 8 and pieces[new_row][new_col].islower() != pieces[row][col].islower() and pieces[new_row][new_col]:
                            all_moves_for_check.append((new_row, new_col))

                if piece == 'k':
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            new_row, new_col = row + i, col + j
                            if 0 <= new_row < 8 and 0 <= new_col < 8 and (i != 0 or j != 0) and pieces[new_row][new_col]:
                                if pieces[new_row][new_col].islower() != pieces[row][col].islower():

                                    all_moves_for_check.append((new_row, new_col))
                if piece == 'p':
                    if 0 <= col - 1 < 8:
                        if 0 <= row + current_turn < 8:
                            if pieces[row + current_turn][col - 1].islower() != pieces[row][col].islower():
                                if pieces[row+current_turn][col-1]:
                                    all_moves_for_check.append((row + current_turn, col - 1))

                    if 0 <= col + 1 < 8 and 0 <= row + current_turn < 8 and pieces[row + current_turn][col + 1].islower() != pieces[row][col].islower() and pieces[row+current_turn][col+1]:
                        all_moves_for_check.append((row + current_turn, col + 1))

                if (piece == 'r' or piece == 'q'):
                    for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        i, j = direction
                        for step in range(1, 8):
                            new_row, new_col = row + (i * step), col + (j * step)
                            if 0 <= new_row < 8 and 0 <= new_col < 8:
                                if pieces[new_row][new_col] == '':
                                    continue
                                elif pieces[new_row][new_col].islower() != pieces[row][col].islower():

                                    all_moves_for_check.append((new_row, new_col))
                                    break
                                else:
                                    break
                            else:
                                break
                if (piece == 'b' or piece == 'q'):
                    for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                        i, j = direction
                        for step in range(1, 8):
                            new_row, new_col = row + (i * step), col + (j * step)
                            if 0 <= new_row < 8 and 0 <= new_col < 8:
                                if pieces[new_row][new_col] == '':
                                    continue
                                elif pieces[new_row][new_col].islower() != pieces[row][col].islower():

                                    all_moves_for_check.append((new_row, new_col))
                                    break
                                else:
                                    break
                            else:
                                break
            if current_turn == -1:
                if pieces[row][col] == 'N':
                    for move in knight_moves:
                        new_row, new_col = row + move[0], col + move[1]
                        if 0 <= new_row < 8 and 0 <= new_col < 8 and pieces[new_row][new_col].islower() != pieces[row][col].islower() and pieces[new_row][new_col]:
                            all_moves_for_check.append((new_row, new_col))

                if piece == 'K':
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            new_row, new_col = row + i, col + j
                            if 0 <= new_row < 8 and 0 <= new_col < 8 and (i != 0 or j != 0) and pieces[new_row][new_col]:
                                if pieces[new_row][new_col].islower() != pieces[row][col].islower():

                                    all_moves_for_check.append((new_row, new_col))
                if piece == 'P':

                    if 0 <= col - 1 < 8 and 0 <= row + current_turn < 8 and pieces[row + current_turn][
                        col - 1].islower() != pieces[row][col].islower() and pieces[row+current_turn][col-1]:
                        all_moves_for_check.append((row + current_turn, col - 1))

                    if 0 <= col + 1 < 8 and 0 <= row + current_turn < 8 and pieces[row + current_turn][col + 1].islower() != pieces[row][col].islower() and pieces[row+current_turn][col+1]:
                        all_moves_for_check.append((row + current_turn, col + 1))

                if (piece == 'R' or piece == 'Q'):
                    for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        i, j = direction
                        for step in range(1, 8):
                            new_row, new_col = row + (i * step), col + (j * step)
                            if 0 <= new_row < 8 and 0 <= new_col < 8:
                                if pieces[new_row][new_col] == '':
                                    continue
                                elif pieces[new_row][new_col].islower() != pieces[row][col].islower():

                                    all_moves_for_check.append((new_row, new_col))
                                    break
                                else:
                                    break
                            else:
                                break
                if (piece == 'B' or piece == 'Q'):
                    for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                        i, j = direction
                        for step in range(1, 8):
                            new_row, new_col = row + (i * step), col + (j * step)
                            if 0 <= new_row < 8 and 0 <= new_col < 8:
                                if pieces[new_row][new_col] == '':
                                    continue
                                elif pieces[new_row][new_col].islower() != pieces[row][col].islower():

                                    all_moves_for_check.append((new_row, new_col))
                                    break
                                else:
                                    break
                            else:
                                break
    # print('all possible attacks: ', all_moves_for_check)
    return all_moves_for_check

def execute_and_check(pieces, row, col, current_turn, new_row, new_col, selected_piece):
    new_white_king_pos = white_king_pos
    new_black_king_pos = black_king_pos
    target_pieces = copy.deepcopy(pieces)
    target_pieces[row][col] = ""
    target_pieces[new_row][new_col] = selected_piece
    if selected_piece == "K":
        new_white_king_pos = (new_row, new_col)
    if selected_piece == "k":
        new_black_king_pos = (new_row, new_col)
    attack_moves = attacks_opponent(target_pieces, current_turn)
    if is_in_check(current_turn, attack_moves, new_white_king_pos, new_black_king_pos):
        return True
    else:
        return False

def calculate_moves(pieces, row, col, selected_piece, last_move, last_moved_piece, current_turn):
    left_castle = True
    right_castle = True
    legal_moves = []
    en_passant_target = None
    castle_target_left = None
    castle_target_right = None
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    if selected_piece.lower() == 'n':
        for move in knight_moves:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8 and (pieces[new_row][new_col] == "" or pieces[new_row][new_col].islower() != selected_piece.islower()):
                if not execute_and_check(pieces, row, col, current_turn, new_row, new_col, selected_piece):
                    legal_moves.append((new_row,new_col))
    if selected_piece.lower() == 'p':
        if 0 <= row - current_turn < 8:
            if pieces[row - current_turn][col] == '':
                # Move one square forward
                if not execute_and_check(pieces, row, col, current_turn, row-current_turn, col, selected_piece):
                    legal_moves.append((row - current_turn, col))
            if 0 <= col - 1 < 8 and pieces[row - current_turn][col - 1] and pieces[row - current_turn][
                col - 1].islower() != pieces[row][col].islower():
                # Capture to the left
                if not execute_and_check(pieces, row, col, current_turn, row-current_turn, col-1, selected_piece):
                    legal_moves.append((row - current_turn, col-1))
            if 0 <= col + 1 < 8 and pieces[row - current_turn][col + 1] and pieces[row - current_turn][
                col + 1].islower() != pieces[row][col].islower():
                # Capture to the right
                if not execute_and_check(pieces, row, col, current_turn, row-current_turn, col+1, selected_piece):
                    legal_moves.append((row - current_turn, col+1))
        if last_move is not None and abs(last_move[0][0] - last_move[1][0]) == 2 and last_move[1][1] == col + 1\
                and pieces[row][col].islower() != pieces[row][col+1].islower() and last_moved_piece.lower() == 'p':
            # Check if the target square is empty (no pawn to capture)
            if pieces[row - current_turn][col + 1] == '':
                if not execute_and_check(pieces, row, col, current_turn, row-current_turn, col+1, selected_piece):
                    legal_moves.append((row - current_turn, col+1))
                    en_passant_target = (row, col + 1)
        if last_move is not None and abs(last_move[0][0] - last_move[1][0]) == 2 and last_move[1][1] == col - 1\
                and pieces[row][col].islower() != pieces[row][col-1].islower() and last_moved_piece.lower() == 'p':
            if pieces[row - current_turn][col - 1] == '':
                if not execute_and_check(pieces, row, col, current_turn, row-current_turn, col-1, selected_piece):
                    legal_moves.append((row - current_turn, col-1))
                    en_passant_target = (row, col - 1)

        if selected_piece == "P" and row == 6 and pieces[row - current_turn][col] == '' and \
                pieces[row - current_turn*2][col] == '':
            if not execute_and_check(pieces, row, col, current_turn, row - current_turn * 2, col, selected_piece):
                legal_moves.append((row - current_turn * 2, col))
        if selected_piece == "p" and row == 1 and pieces[row - current_turn][col] == '' and \
                pieces[row - current_turn * 2][col] == '':
            if not execute_and_check(pieces, row, col, current_turn, row - current_turn * 2, col, selected_piece):
                legal_moves.append((row - current_turn * 2, col))
    if (selected_piece.lower() == 'r' or selected_piece.lower() == 'q'):
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            i, j = direction
            for step in range(1, 8):
                new_row, new_col = row + (i * step), col + (j * step)
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if pieces[new_row][new_col] == '':
                        if not execute_and_check(pieces, row, col, current_turn, new_row, new_col, selected_piece):
                            legal_moves.append((new_row, new_col))
                    elif pieces[new_row][new_col].islower() != pieces[row][col].islower():
                        if not execute_and_check(pieces, row, col, current_turn, new_row, new_col, selected_piece):
                            legal_moves.append((new_row, new_col))
                        break
                    else:
                        break
                        if not execute_and_check(pieces, row, col, current_turn, new_row, new_col, selected_piece):
                            legal_moves.append((new_row, new_col))
                else:
                    break
    if (selected_piece.lower() == 'b' or selected_piece.lower() == 'q'):
        for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            i, j = direction
            for step in range(1, 8):
                new_row, new_col = row + (i * step), col + (j * step)
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if pieces[new_row][new_col] == '':
                        if not execute_and_check(pieces, row, col, current_turn, new_row, new_col, selected_piece):
                            legal_moves.append((new_row, new_col))
                    elif pieces[new_row][new_col].islower() != pieces[row][col].islower():
                        if not execute_and_check(pieces, row, col, current_turn, new_row, new_col, selected_piece):
                            legal_moves.append((new_row, new_col))
                        break
                    else:
                        break
                        if not execute_and_check(pieces, row, col, current_turn, new_row, new_col, selected_piece):
                            legal_moves.append((new_row, new_col))
                else:
                    break
    if selected_piece.lower() == 'k':
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_row, new_col = row + i, col + j
                if 0 <= new_row < 8 and 0 <= new_col < 8 and (i != 0 or j != 0):
                    if pieces[new_row][new_col] == "" or pieces[new_row][new_col].islower() != pieces[row][col].islower():
                        if not execute_and_check(pieces, row, col, current_turn, new_row, new_col, selected_piece):
                            legal_moves.append((new_row, new_col))
        if not black_king_moved and not lbr_moved and not pieces[row][col-1] and not pieces[row][col-2] and current_turn == - 1:
            for i in range(3):
                if execute_and_check(pieces, row, col, current_turn, row, col-i, selected_piece):
                    left_castle = False
                    break
            if left_castle:
                legal_moves.append((row, col-2))
                castle_target_left = ((row, col-1))
        if not black_king_moved and not rbr_moved and not pieces[row][col+1] and not pieces[row][col+2] and current_turn == -1:
            for i in range(3):
                if execute_and_check(pieces, row, col, current_turn, row, col+i, selected_piece):
                    right_castle = False
                    break
            if right_castle:
                legal_moves.append((row, col+2))
                castle_target_right = ((row, col + 1))

        if not white_king_moved and not lwr_moved and not pieces[row][col-1] and not pieces[row][col-2] and current_turn == 1:
            for i in range(3):
                if execute_and_check(pieces, row, col, current_turn, row, col-i, selected_piece):
                    left_castle = False
                    break
            if left_castle:
                legal_moves.append((row, col-2))
                castle_target_left = ((row, col-1))
        if not white_king_moved and not rwr_moved and not pieces[row][col+1] and not pieces[row][col+2] and current_turn == 1:
            for i in range(3):
                if execute_and_check(pieces, row, col, current_turn, row, col+i, selected_piece):
                    print(right_castle)
                    right_castle = False
                    break
            if right_castle:
                legal_moves.append((row, col+2))
                castle_target_right = ((row, col + 1))

    return legal_moves, en_passant_target, castle_target_left, castle_target_right

def is_in_check(current_turn, all_moves, white_king_pos, black_king_pos):
    king_position = white_king_pos if current_turn == 1 else black_king_pos
    if king_position in all_moves:
        return True  # The king is in check
    # print("Not in check")
    return False  # The king is not in check

def check_for_checkmate(pieces, current_turn, last_move, last_moved_piece):
    all_legal_moves = []
    for row in range(8):
        for col in range(8):
            if current_turn == 1:
                if pieces[row][col].isupper():
                    selected_piece = pieces[row][col]
                    moves, en_passant_target, _, _ = calculate_moves(pieces, row, col, selected_piece, last_move, last_moved_piece, current_turn)
                    if moves:
                        all_legal_moves.append(moves)
            if current_turn == -1:
                if pieces[row][col].islower():
                    selected_piece = pieces[row][col]
                    moves, en_passant_target, _, _ = calculate_moves(pieces, row, col, selected_piece, last_move, last_moved_piece, current_turn)
                    if moves:
                        all_legal_moves.append(moves)
    # print(all_legal_moves)
    if not all_legal_moves:
        print('Checkmate!')
        return True
    else:
        return False

def promote(selected_piece, pieces, row, col, selected_position):
    print('Promote!')
    screen.blit(promotion_screen, promotion_screen_rect.topleft)
    if selected_piece.islower():
        options = ['q', 'r', 'b', 'n']
    else:
        options = ['Q', 'R', 'B', 'N']
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for i, option in enumerate(options):
                    rect = pygame.Rect(promotion_screen_rect.left + 20 + i * 60, promotion_screen_rect.top + 20, 60, 60)
                    if rect.collidepoint(x, y):
                        print(option)
                        return option

        screen.blit(promotion_screen, promotion_screen_rect.topleft)
        for i, option in enumerate(options):
            image = images[option]
            x = promotion_screen_rect.left + 20 + i * 60 + 15
            y = promotion_screen_rect.top + 20 + 15
            screen.blit(image, (x,y))
            pygame.draw.rect(screen, (0, 0, 0), (x - 5, y - 5, 60, 60), 2)

        pygame.display.flip()

def check_stalemate(pieces):
    black_pieces_left = []
    white_pieces_left = []
    for row in range(8):
        for col in range(8):
            if pieces[row][col].islower():
                black_pieces_left.append(pieces[row][col])
            if pieces[row][col].isupper():
                white_pieces_left.append(pieces[row][col])
    if (black_pieces_left == ['k'] or set(black_pieces_left) == {'k', 'n'} or set(black_pieces_left) == {'k', 'b'}) and (white_pieces_left == ['K'] or set(white_pieces_left) == {'K', 'N'} or set(white_pieces_left) == {'K', 'B'}):
        return True
    else:
        return False


# Draw the chessboard
def draw_chessboard(screen, chessboard, pieces, legal_moves, message):
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQAURE_SIZE, row * SQAURE_SIZE, SQAURE_SIZE, SQAURE_SIZE))
            piece = pieces[row][col]
            if piece:
                piece_image = images[piece]
                screen.blit(piece_image, (col * SQAURE_SIZE, row * SQAURE_SIZE))

    for move in legal_moves if legal_moves else []:
        pygame.draw.circle(screen, LEGAL_MOVE_COLOR, (move[1]*SQAURE_SIZE + SQAURE_SIZE // 2, move[0]*SQAURE_SIZE + SQAURE_SIZE //2), 10)
    # Update the display
    if message:
        show_message_box(message)
    message = None
    pygame.display.flip()

draw_chessboard(screen, chessboard, pieces, legal_moves, message)
# Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            col = x // SQAURE_SIZE
            row = y // SQAURE_SIZE
            if event.button == 1:

                #Select a piece
                if selected_piece == None or (selected_piece.isupper() and pieces[row][col].isupper()) or (selected_piece.islower() and pieces[row][col].islower()):
                    if pieces[row][col] != '' and ((current_turn == 1 and pieces[row][col].isupper()) or (current_turn == -1 \
                            and pieces[row][col].islower())):
                        selected_piece = pieces[row][col]
                        legal_moves, en_passant_target, castle_left_target, castle_right_target = calculate_moves(pieces, row, col, selected_piece, last_move, last_moved_piece, current_turn)
                        selected_position = (row, col)
                # Move a piece
                else:
                    if (current_turn == 1 and pieces[row][col].islower() or pieces[row][col] == "") or ((current_turn == -1 and pieces[row][col].isupper()) or pieces[row][col] == ""):
                        if (row, col) in legal_moves if legal_moves else []:
                            if en_passant_target is not None:
                                if en_passant_target[1] == col:
                                    pieces[en_passant_target[0]][en_passant_target[1]] = ''
                            if castle_left_target is not None and current_turn == 1:
                                if castle_left_target[1] == col+1:
                                    pieces[castle_left_target[0]][castle_left_target[1]] = 'R'
                                    pieces[7][0] = ''
                                    lwr_moved = True
                            if castle_right_target is not None and current_turn == 1:
                                if castle_right_target[1] == col-1:
                                    pieces[castle_right_target[0]][castle_right_target[1]] = 'R'
                                    pieces[7][7] = ''
                                    rwr_moved = True
                            if castle_left_target is not None and current_turn == -1:
                                if castle_left_target[1] == col+1:
                                    pieces[castle_left_target[0]][castle_left_target[1]] = 'r'
                                    pieces[0][0] = ''
                                    lbr_moved = True
                            if castle_right_target is not None and current_turn == -1:
                                if castle_right_target[1] == col-1:
                                    pieces[castle_right_target[0]][castle_right_target[1]] = 'r'
                                    pieces[0][7] = ''
                                    rbr_moved = True
                            pieces[selected_position[0]][selected_position[1]] = ""
                            pieces[row][col] = selected_piece
                            if selected_piece == 'p' and row == 7:
                                pieces[row][col] = promote(selected_piece, pieces, row, col, selected_position)
                            if selected_piece == 'P' and row == 0:
                                pieces[row][col] = promote(selected_piece, pieces, row, col, selected_position)
                            if selected_piece == 'r' :
                                if selected_position[1] == 0:
                                    lbr_moved = True
                                if selected_position[1] == 7:
                                    rbr_moved = True
                            if selected_piece == 'R' :
                                if selected_position[1] == 0:
                                    lwr_moved = True
                                if selected_position[1] == 7:
                                    rwr_moved = True
                            if selected_piece == "K":
                                white_king_pos = (row, col)
                                white_king_moved = True
                            elif selected_piece == 'k':
                                black_king_pos = (row, col)
                                black_king_moved = True
                            current_turn *= -1 # Switch turn after each move
                    last_moved_piece = selected_piece
                    last_move = ((row, col), (selected_position[0], selected_position[1]))
                    selected_piece = None
                    selected_position = None
                    legal_moves = None

            elif event.button == 3:  # Right mouse button
                selected_piece = None
                selected_position = None
                legal_moves = None

            attack_moves = attacks_opponent(pieces, current_turn)
            if check_for_checkmate(pieces, current_turn, last_move, last_moved_piece):
                if is_in_check(current_turn, attack_moves, white_king_pos, black_king_pos):
                    print('Actual Checkmate')
                    message = 'Checkmate!'
                else:
                    print('Stalemate')
                    message = 'Stalemate!'
            if check_stalemate(pieces):
                print('Insufficient Material')
                message = 'Insufficient Material'
            draw_chessboard(screen, chessboard, pieces, legal_moves, message)

pygame.quit()