from enum import Enum
import pygame
from const import ChessConst


class PositionColor(Enum):
    WHITE = (255, 255, 255)
    BLACK = (255, 0, 0)
    SELECTED = (0,255,0)


class Position:
    def __init__(self, xy, position_color):
        self.position_color = position_color
        self.position = xy

    def draw(self, screen):
        x = ChessConst.START_CORNER[0] + self.position[0] * ChessConst.FIELD_SIZE[0]
        y = ChessConst.START_CORNER[1] + self.position[1] * ChessConst.FIELD_SIZE[1]
        if self.position_color == PositionColor.WHITE:
            color = (255, 255, 255)
        elif self.position_color == PositionColor.BLACK:
            color = ChessConst.BLACK_FIELD_COLOR
        else:
            color = ChessConst.POSSIBLE_FIELD_COLOR
        pygame.draw.rect(screen, color, pygame.Rect(x, y,ChessConst.FIELD_SIZE[0],ChessConst.FIELD_SIZE[1]))
