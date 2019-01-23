import pygame
from enum import Enum
from const import ChessConst


def position_in_list(pos, lst):
    return len(list(filter(lambda p: p.position[1] == pos[1] and p.position[0] == pos[0], lst))) > 0

class FigureColor(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


class Figure:
    def __init__(self, xy, figure_color):
        self.position = xy
        self.color = figure_color
        self.first_move = False
        self.en_passant_pos = None

    def calculate_possible_moves(self, mines, theirs): raise NotImplementedError

    def draw(self, screen): raise NotImplementedError


class Pawn(Figure):
    def __init__(self, xy, figure_color):
        super().__init__(xy, figure_color)

        if self.color == FigureColor.WHITE:
            self.image = pygame.image.load('images/Chess_plt45.svg.png')
        else:
            self.image = pygame.image.load('images/1024px-Chess_pdt45.svg.png')
        self.image = pygame.transform.scale(self.image, ChessConst.FIELD_SIZE)

    def calculate_possible_moves(self, mines, theirs):
        possible_moves = []
        if self.color == FigureColor.WHITE:
            y_move = -1
        else:
            y_move = 1

        for field in theirs:
            if field.position[0] == self.position[0] - 1 and field.position[1] == self.position[1] + y_move:
                possible_moves.append(field.position)
                break

        for field in theirs:
            if field.position[0] == self.position[0] + 1 and field.position[1] == self.position[1] + y_move:
                possible_moves.append(field.position)
                break

        for field in theirs:
            if field.en_passant_pos is not None and field.en_passant_pos[0] == self.position[0] - 1 and field.en_passant_pos[1] == self.position[1] + y_move:
                possible_moves.append(field.en_passant_pos)
                break

        for field in theirs:
            if field.en_passant_pos is not None and field.en_passant_pos[0] == self.position[0] + 1 and field.en_passant_pos[1] == self.position[1] + y_move:
                possible_moves.append(field.en_passant_pos)
                break

        for field in mines:
            if field.position[1] == self.position[1] + y_move and field.position[0] == self.position[0]:
                return possible_moves
        for field in theirs:
            if field.position[1] == self.position[1] + y_move and field.position[0] == self.position[0]:
                return possible_moves

        possible_moves.append((self.position[0], self.position[1] + y_move))

        for field in mines:
            if field.position[1] == self.position[1] + y_move + y_move and field.position[0] == self.position[0]:
                return possible_moves
        for field in theirs:
            if field.position[1] == self.position[1] + y_move + y_move and field.position[0] == self.position[0]:
                return possible_moves

        if not self.first_move:
            possible_moves.append((self.position[0], self.position[1] + y_move + y_move))

        return possible_moves

    def draw(self, screen):
        x = ChessConst.START_CORNER[0] + self.position[0] * ChessConst.FIELD_SIZE[0]
        y = ChessConst.START_CORNER[1] + self.position[1] * ChessConst.FIELD_SIZE[1]
        screen.blit(self.image, (x, y))


class Tower(Figure):
    def __init__(self, xy, figure_color):
        super().__init__(xy, figure_color)

        if self.color == FigureColor.WHITE:
            self.image = pygame.image.load('images/1024px-Chess_rlt45.svg.png')
        else:
            self.image = pygame.image.load('images/Chess_rdt45.svg.png')
        self.image = pygame.transform.scale(self.image, ChessConst.FIELD_SIZE)

    def calculate_possible_moves(self, mines, theirs):
        possible_moves = []

        for i in range(self.position[0]+1,8):
            if len(list(filter(lambda p: p.position[0] == i and p.position[1] == self.position[1], mines))) > 0:
                break
            possible_moves.append((i, self.position[1]))
            if len(list(filter(lambda p: p.position[0] == i and p.position[1] == self.position[1], theirs))) > 0:
                break
        for i in range(self.position[1]+1,8):
            if len(list(filter(lambda p: p.position[1] == i and p.position[0] == self.position[0], mines))) > 0:
                break
            possible_moves.append((self.position[0], i))
            if len(list(filter(lambda p: p.position[1] == i and p.position[0] == self.position[0], theirs))) > 0:
                break
        for i in range(self.position[0]-1,-1,-1):
            if len(list(filter(lambda p: p.position[0] == i and p.position[1] == self.position[1], mines))) > 0:
                break
            possible_moves.append((i, self.position[1]))
            if len(list(filter(lambda p: p.position[0] == i and p.position[1] == self.position[1], theirs))) > 0:
                break
        for i in range(self.position[1]-1,-1,-1):
            if len(list(filter(lambda p: p.position[1] == i and p.position[0] == self.position[0], mines))) > 0:
                break
            possible_moves.append((self.position[0], i))
            if len(list(filter(lambda p: p.position[1] == i and p.position[0] == self.position[0], theirs))) > 0:
                break

        return possible_moves


    def draw(self, screen):
        x = ChessConst.START_CORNER[0] + self.position[0] * ChessConst.FIELD_SIZE[0]
        y = ChessConst.START_CORNER[1] + self.position[1] * ChessConst.FIELD_SIZE[1]
        screen.blit(self.image, (x, y))


class Horse(Figure):
    def __init__(self, xy, figure_color):
        super().__init__(xy, figure_color)

        if self.color == FigureColor.WHITE:
            self.image = pygame.image.load('images/1024px-Chess_nlt45.svg.png')
        else:
            self.image = pygame.image.load('images/1024px-Chess_ndt45.svg.png')
        self.image = pygame.transform.scale(self.image, ChessConst.FIELD_SIZE)

    def calculate_possible_moves(self, mines, theirs):
        possible_moves = []

        hops = (2,-2)
        moves = (1,-1)
        for i in hops:
            for j in moves:
                possible_moves.append((self.position[0] + i, self.position[1] + j))
                possible_moves.append((self.position[0] + j, self.position[1] + i))
        possible_moves = list(filter(lambda x: x[0] >= 0 and  x[1] >= 0 and x[0] < 8 and  x[1] < 8, possible_moves))
        possible_moves = \
            list(filter(lambda x:
                        len(list(filter(lambda z: z.position[0] == x[0] and z.position[1] == x[1], mines))) == 0, possible_moves))

        return possible_moves

    def draw(self, screen):
        x = ChessConst.START_CORNER[0] + self.position[0] * ChessConst.FIELD_SIZE[0]
        y = ChessConst.START_CORNER[1] + self.position[1] * ChessConst.FIELD_SIZE[1]
        screen.blit(self.image, (x, y))


class Bishop(Figure):
    def __init__(self, xy, figure_color):
        super().__init__(xy, figure_color)

        if self.color == FigureColor.WHITE:
            self.image = pygame.image.load('images/Chess_blt45.svg.png')
        else:
            self.image = pygame.image.load('images/1024px-Chess_bdt45.svg.png')
        self.image = pygame.transform.scale(self.image, ChessConst.FIELD_SIZE)

    def calculate_possible_moves(self, mines, theirs):
        possible_moves = []

        for i in range(1, 8):
            pos = (self.position[0] + i, self.position[1] + i)
            if position_in_list(pos, mines):
                break
            possible_moves.append(pos)
            if position_in_list(pos, theirs):
                break

        for i in range(1, 8):
            pos = (self.position[0] - i, self.position[1] - i)
            if position_in_list(pos, mines):
                break
            possible_moves.append(pos)
            if position_in_list(pos, theirs):
                break

        for i in range(1, 8):
            pos = (self.position[0] + i, self.position[1] - i)
            if position_in_list(pos, mines):
                break
            possible_moves.append(pos)
            if position_in_list(pos, theirs):
                break

        for i in range(1, 8):
            pos = (self.position[0] - i, self.position[1] + i)
            if position_in_list(pos, mines):
                break
            possible_moves.append(pos)
            if position_in_list(pos, theirs):
                break

        possible_moves = list(filter(lambda x: x[0] >= 0 and x[1] >= 0 and x[0] < 8 and x[1] < 8, possible_moves))
        return possible_moves

    def draw(self, screen):
        x = ChessConst.START_CORNER[0] + self.position[0] * ChessConst.FIELD_SIZE[0]
        y = ChessConst.START_CORNER[1] + self.position[1] * ChessConst.FIELD_SIZE[1]
        screen.blit(self.image, (x, y))


class Queen(Figure):
    def __init__(self, xy, figure_color):
        super().__init__(xy, figure_color)

        if self.color == FigureColor.WHITE:
            self.image = pygame.image.load('images/Chess_qlt45.svg.png')
        else:
            self.image = pygame.image.load('images/1024px-Chess_qdt45.svg.png')
        self.image = pygame.transform.scale(self.image, ChessConst.FIELD_SIZE)

    def calculate_possible_moves(self, mines, theirs):
        possible_moves = []
        possible_moves = []

        for i in range(self.position[0] + 1, 8):
            if len(list(filter(lambda p: p.position[0] == i and p.position[1] == self.position[1], mines))) > 0:
                break
            possible_moves.append((i, self.position[1]))
            if len(list(filter(lambda p: p.position[0] == i and p.position[1] == self.position[1], theirs))) > 0:
                break
        for i in range(self.position[1] + 1, 8):
            if len(list(filter(lambda p: p.position[1] == i and p.position[0] == self.position[0], mines))) > 0:
                break
            possible_moves.append((self.position[0], i))
            if len(list(filter(lambda p: p.position[1] == i and p.position[0] == self.position[0], theirs))) > 0:
                break
        for i in range(self.position[0] - 1, -1, -1):
            if len(list(filter(lambda p: p.position[0] == i and p.position[1] == self.position[1], mines))) > 0:
                break
            possible_moves.append((i, self.position[1]))
            if len(list(filter(lambda p: p.position[0] == i and p.position[1] == self.position[1], theirs))) > 0:
                break
        for i in range(self.position[1] - 1, -1, -1):
            if len(list(filter(lambda p: p.position[1] == i and p.position[0] == self.position[0], mines))) > 0:
                break
            possible_moves.append((self.position[0], i))
            if len(list(filter(lambda p: p.position[1] == i and p.position[0] == self.position[0], theirs))) > 0:
                break

        for i in range(1, 8):
            pos = (self.position[0] + i, self.position[1] + i)
            if position_in_list(pos, mines):
                break
            possible_moves.append(pos)
            if position_in_list(pos, theirs):
                break

        for i in range(1, 8):
            pos = (self.position[0] - i, self.position[1] - i)
            if position_in_list(pos, mines):
                break
            possible_moves.append(pos)
            if position_in_list(pos, theirs):
                break

        for i in range(1, 8):
            pos = (self.position[0] + i, self.position[1] - i)
            if position_in_list(pos, mines):
                break
            possible_moves.append(pos)
            if position_in_list(pos, theirs):
                break

        for i in range(1, 8):
            pos = (self.position[0] - i, self.position[1] + i)
            if position_in_list(pos, mines):
                break
            possible_moves.append(pos)
            if position_in_list(pos, theirs):
                break

        possible_moves = list(filter(lambda x: x[0] >= 0 and x[1] >= 0 and x[0] < 8 and x[1] < 8, possible_moves))
        return possible_moves

    def draw(self, screen):
        x = ChessConst.START_CORNER[0] + self.position[0] * ChessConst.FIELD_SIZE[0]
        y = ChessConst.START_CORNER[1] + self.position[1] * ChessConst.FIELD_SIZE[1]
        screen.blit(self.image, (x, y))


class King(Figure):
    def __init__(self, xy, figure_color):
        super().__init__(xy, figure_color)

        if self.color == FigureColor.WHITE:
            self.image = pygame.image.load('images/Chess_klt45.svg.png')
        else:
            self.image = pygame.image.load('images/1024px-Chess_kdt45.svg.png')
        self.image = pygame.transform.scale(self.image, ChessConst.FIELD_SIZE)

    def calculate_possible_moves(self, mines, theirs):
        possible_moves = []

        for i in range(-1,2):
            for j in range(-1, 2):
                if not position_in_list((self.position[0] + i, self.position[1] + j), mines):
                    possible_moves.append((self.position[0] + i, self.position[1] + j))

        if not self.first_move:
            if not position_in_list((self.position[0] + 1, self.position[1]), mines):
                if not position_in_list((self.position[0] + 2, self.position[1]), mines):
                    if not position_in_list((self.position[0] + 1, self.position[1]), theirs):
                        if not position_in_list((self.position[0] + 2, self.position[1]), theirs):
                            if len(list(filter(lambda x: isinstance(x, Tower) and not x.first_move
                                                      and x.position[0] == self.position[0]+3
                                                      and x.position[1] == x.position[1], mines))) > 0:
                                possible_moves.append((self.position[0] + 2, self.position[1]))

        possible_moves = list(filter(lambda x: x[0] >= 0 and x[1] >= 0 and x[0] < 8 and x[1] < 8, possible_moves))
        return possible_moves

    def draw(self, screen):
        x = ChessConst.START_CORNER[0] + self.position[0] * ChessConst.FIELD_SIZE[0]
        y = ChessConst.START_CORNER[1] + self.position[1] * ChessConst.FIELD_SIZE[1]
        screen.blit(self.image, (x, y))


