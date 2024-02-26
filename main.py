import numpy as np
import pygame
import sys
import engine
import alg_ai
import neuro


class draw:
    WIDTH = HEIGHT = 600
    LINE_WIDTH = 15
    BOARD_ROWS = BOARD_COLS = 3
    SQUARE_SIZE = WIDTH // BOARD_ROWS
    CIRCLE_RADIUS = SQUARE_SIZE // 3
    CIRCLE_WIDTH = 15
    CROSS_WIDTH = 25
    SPACE = SQUARE_SIZE // 4

    CIRCLE_COLOR = (239, 231, 200)
    CROSS_COLOR = (66, 66, 66)
    BG_COLOR = (28, 170, 156)
    LINE_COLOR = (23, 145, 135)
    @classmethod
    def draw_board(cls):
        screen.fill(cls.BG_COLOR)
        draw._draw_line()

    @classmethod
    def _draw_line(cls):
        pygame.draw.line(screen, cls.LINE_COLOR, (0, cls.SQUARE_SIZE), (cls.WIDTH, cls.SQUARE_SIZE), cls.LINE_WIDTH)
        pygame.draw.line(screen, cls.LINE_COLOR, (0, 2 * cls.SQUARE_SIZE),
                         (cls.WIDTH, 2 * cls.SQUARE_SIZE), cls.LINE_WIDTH)

        pygame.draw.line(screen, cls.LINE_COLOR, (cls.SQUARE_SIZE, 0),
                         (cls.SQUARE_SIZE, cls.WIDTH), cls.LINE_WIDTH)
        pygame.draw.line(screen, cls.LINE_COLOR, (2 * cls.SQUARE_SIZE, 0),
                         (2 * cls.SQUARE_SIZE, cls.WIDTH), cls.LINE_WIDTH)

    @classmethod
    def draw_figures(cls, ttt):
        for row in range(3):
            for col in range(3):
                if ttt.board[row][col] == 1:
                    pygame.draw.line(screen, cls.CROSS_COLOR,
                                     (col * cls.SQUARE_SIZE + cls.SPACE, (row + 1) * cls.SQUARE_SIZE - cls.SPACE),
                                     ((col + 1) * cls.SQUARE_SIZE - cls.SPACE, row * cls.SQUARE_SIZE + cls.SPACE),
                                     cls.CROSS_WIDTH)
                    pygame.draw.line(screen, cls.CROSS_COLOR,
                                     (col * cls.SQUARE_SIZE + cls.SPACE, row * cls.SQUARE_SIZE + cls.SPACE),
                                     ((col + 1) * cls.SQUARE_SIZE - cls.SPACE, (row + 1) * cls.SQUARE_SIZE - cls.SPACE),
                                     cls.CROSS_WIDTH)
                elif ttt.board[row][col] == -1:
                    pygame.draw.circle(screen, cls.CIRCLE_COLOR,
                                       (int((col + 0.5) * cls.SQUARE_SIZE), int((row + 0.5) * cls.SQUARE_SIZE)),
                                       cls.CIRCLE_RADIUS, cls.CIRCLE_WIDTH)

    @classmethod
    def draw_win(cls, ttt, win_tuple):
        if ttt.turn == -1:
            color = cls.CROSS_COLOR
        else:
            color = cls.CIRCLE_COLOR
        match win_tuple[2]:
            case 'row':
                draw._draw_horizontal_winning_line(win_tuple[1], color)
            case 'col':
                draw._draw_vertical_winning_line(win_tuple[1], color)
            case 'diagonal':
                if win_tuple[1] == 1:
                    draw._draw_desc_diagonal_line(color)
                else:
                    draw._draw_asc_diagonal_line(color)

    @classmethod
    def _draw_vertical_winning_line(cls, col, color):
        posX = int((col+0.5) * cls.SQUARE_SIZE)
        pygame.draw.line(screen, color, (posX, 15), (posX, cls.HEIGHT - 15), 15)

    @classmethod
    def _draw_horizontal_winning_line(cls, row, color):
        posY = int((row+0.5) * cls.SQUARE_SIZE)
        pygame.draw.line(screen, color, (15, posY), (cls.WIDTH - 15, posY), 15)

    @classmethod
    def _draw_asc_diagonal_line(cls, color):
        pygame.draw.line(screen, color, (15, cls.HEIGHT - 15), (cls.WIDTH - 15, 15), 15)

    @classmethod
    def _draw_desc_diagonal_line(cls, color):
        pygame.draw.line(screen, color, (15, 15), (cls.WIDTH - 15, cls.HEIGHT - 15), 15)


def main(first_player, second_player):
    ttt = engine.TicTacToe(np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]), 1)
    game_over = False
    running = True
    move_maid = False
    while running:
        human_turn = (ttt.turn == 1 and first_player == 1) or (ttt.turn == -1 and second_player == 1)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    ttt.undo_move()
                    draw.draw_board()
                    move_maid = False
                    game_over = False
                elif e.key == pygame.K_r:
                    running = False
                    break
                elif e.key == pygame.K_d:
                    if len(ttt.move_log) >= 2:
                        ttt.undo_move()
                        ttt.undo_move()
                        draw.draw_board()
                        move_maid = False
                        game_over = False

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    location = e.pos
                    move = (location[1]//draw.SQUARE_SIZE, location[0] // draw.SQUARE_SIZE)
                    if move in ttt.valid_moves:
                        ttt.make_move(move)
                        move_maid = True

        if not game_over and not human_turn:
            neuro_turn = (ttt.turn == 1 and first_player == 3) or (ttt.turn == -1 and second_player == 3)
            if neuro_turn:
                move = model.best_move(ttt)[1]
            else:
                move = alg_ai.find_best_move(ttt)[1]
            ttt.make_move(move)
            move_maid = True

        if move_maid:
            move_maid = False
            win_tuple = ttt.winned()
            if win_tuple[0]:
                draw.draw_win(ttt, win_tuple)
                game_over = True
            if ttt.drow():
                game_over = True
        draw.draw_figures(ttt)

        pygame.display.update()


if __name__ == '__main__':
    model = neuro.neuro_model()
    pygame.init()
    screen = pygame.display.set_mode((draw.WIDTH, draw.HEIGHT))
    pygame.display.set_caption('TIC TAC TOE')
    while True:
        draw.draw_board()
        pygame.display.update()
        first_player = int(input('Кто будет играть за X(1 - человек/2 - алгоритм/3 - нейросеть): '))
        second_player = int(input('Кто будет играть за O(1 - человек/2 - алгоритм/3 - нейросеть): '))
        main(first_player, second_player)
