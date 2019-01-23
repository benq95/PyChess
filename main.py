import pygame
from pygame.locals import *
from figures import *
from position import *


class App:


    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 600, 600
        self.positions = []
        self.blacks = []
        self.whites = []
        self.current_player = FigureColor.WHITE
        self.selected_figure = None
        self.check_black = False
        self.check_white = False
        self.winner = None

    def init_board(self):
        self.positions = []

        color = PositionColor.WHITE

        for i in range(0,8):

            for j in range(0,8):
                field = Position((i,j),color)
                # field.draw(self._display_surf)
                self.positions.append(field)

                if color == PositionColor.WHITE:
                    color = PositionColor.BLACK
                else:
                    color = PositionColor.WHITE

            if color == PositionColor.WHITE:
                color = PositionColor.BLACK
            else:
                color = PositionColor.WHITE

    def init_figures(self):
        self.blacks = []
        self.whites = []

        # towers
        figure = Tower((0, 0), FigureColor.BLACK)
        figure.draw(self._display_surf)
        self.blacks.append(figure)
        figure = Tower((7, 0), FigureColor.BLACK)
        figure.draw(self._display_surf)
        self.blacks.append(figure)

        figure = Tower((0, 7), FigureColor.WHITE)
        figure.draw(self._display_surf)
        self.whites.append(figure)
        figure = Tower((7, 7), FigureColor.WHITE)
        figure.draw(self._display_surf)
        self.whites.append(figure)

        # horses
        figure = Horse((1, 0), FigureColor.BLACK)
        figure.draw(self._display_surf)
        self.blacks.append(figure)
        figure = Horse((6, 0), FigureColor.BLACK)
        figure.draw(self._display_surf)
        self.blacks.append(figure)

        figure = Horse((1, 7), FigureColor.WHITE)
        figure.draw(self._display_surf)
        self.whites.append(figure)
        figure = Horse((6, 7), FigureColor.WHITE)
        figure.draw(self._display_surf)
        self.whites.append(figure)

        # bishops
        figure = Bishop((2, 0), FigureColor.BLACK)
        figure.draw(self._display_surf)
        self.blacks.append(figure)
        figure = Bishop((5, 0), FigureColor.BLACK)
        figure.draw(self._display_surf)
        self.blacks.append(figure)

        figure = Bishop((2, 7), FigureColor.WHITE)
        figure.draw(self._display_surf)
        self.whites.append(figure)
        figure = Bishop((5, 7), FigureColor.WHITE)
        figure.draw(self._display_surf)
        self.whites.append(figure)

        # king
        figure = King((4, 0), FigureColor.BLACK)
        figure.draw(self._display_surf)
        self.blacks.append(figure)
        figure = King((4, 7), FigureColor.WHITE)
        figure.draw(self._display_surf)
        self.whites.append(figure)

        # queen
        figure = Queen((3, 0), FigureColor.BLACK)
        figure.draw(self._display_surf)
        self.blacks.append(figure)
        figure = Queen((3, 7), FigureColor.WHITE)
        figure.draw(self._display_surf)
        self.whites.append(figure)

        for i in range(0,8):
            figure = Pawn((i,1), FigureColor.BLACK)
            figure.draw(self._display_surf)
            self.blacks.append(figure)

            figure = Pawn((i, 6), FigureColor.WHITE)
            figure.draw(self._display_surf)
            self.whites.append(figure)

    def resolve_click(self, pos):
        for figure in self.blacks if self.current_player == FigureColor.BLACK else self.whites:
            if figure.position[0] == pos[0] and figure.position[1] == pos[1]:
                self.show_moves(figure)
                return

        for position in self.positions:
            if position.position[0] == pos[0] and position.position[1] == pos[1]:
                if position.position_color == PositionColor.SELECTED:
                    self.move(pos)
                    return

    def move(self, pos):
        self.init_board()

        for figure in self.whites if self.current_player == FigureColor.BLACK else self.blacks:
            if figure.position[0] == pos[0] and figure.position[1] == pos[1]:
                (self.whites if self.current_player == FigureColor.BLACK else self.blacks).remove(figure)
                break

        if isinstance(self.selected_figure, King) and not self.selected_figure.first_move:
            if pos[0] == self.selected_figure.position[0] + 2 and pos[1] == self.selected_figure.position[1]:
                tower = None
                for figure in self.whites if self.current_player == FigureColor.WHITE else self.blacks:
                    if isinstance(figure, Tower) \
                            and figure.position[0] == self.selected_figure.position[0] + 3 \
                            and figure.position[1] == self.selected_figure.position[1]:
                        tower = figure
                tower.position = (pos[0] - 1, pos[1])

        if isinstance(self.selected_figure, Pawn):
            for figure in self.whites if self.current_player == FigureColor.BLACK else self.blacks:
                if figure.en_passant_pos is not None and figure.en_passant_pos[0] == pos[0] and figure.en_passant_pos[1] == pos[1]:
                    (self.whites if self.current_player == FigureColor.BLACK else self.blacks).remove(figure)

        for figure in self.whites if self.current_player == FigureColor.BLACK else self.blacks:
            figure.en_passant_pos = None

        if isinstance(self.selected_figure, Pawn) and not self.selected_figure.first_move:
            if pos[1] - self.selected_figure.position[1] > 1 \
                or pos[1] - self.selected_figure.position[1] < -1:
                self.selected_figure.en_passant_pos \
                    = (self.selected_figure.position[0], int((self.selected_figure.position[1] + pos[1])/2))

        self.selected_figure.position = pos
        self.selected_figure.first_move = True
        self.selected_figure = None
        self.current_player = FigureColor.BLACK if self.current_player == FigureColor.WHITE else FigureColor.WHITE
        for figure in self.blacks:
            if isinstance(figure, King):
                mines = self.whites
                theirs = self.blacks
                for a_figure in self.whites:
                    moves = a_figure.calculate_possible_moves(mines, theirs)
                    found = False
                    for move in moves:
                        if move[0] == figure.position[0] and move[1] == figure.position[1]:
                            # print("Szach czarny")
                            self.check_black = True
                            found = True
                            break
                        self.check_black = False
                    if found:
                        break
                moves = figure.calculate_possible_moves(self.blacks, self.whites)
                for move in moves:
                    temp_pos = figure.position
                    figure.position = move
                    for a_figure in self.whites:
                        sim_moves = a_figure.calculate_possible_moves(mines,theirs)
                        for a_move in sim_moves:
                            if a_move[0] == move[0] and a_move[1] == move[1]:
                                moves = list(filter(lambda x: x[0] != move[0] or x[1] != move[1], moves))
                    figure.position = temp_pos
                if len(moves) == 0 and self.check_black:
                    self.winner = FigureColor.WHITE
                break
        for figure in self.whites:
            if isinstance(figure, King):
                mines = self.blacks
                theirs = self.whites
                for a_figure in self.blacks:
                    moves = a_figure.calculate_possible_moves(mines, theirs)
                    found = False
                    for move in moves:
                        if move[0] == figure.position[0] and move[1] == figure.position[1]:
                            # print("Szach bialy")
                            self.check_white = True
                            found = True
                            break
                        self.check_white = False
                    if found:
                        break
                moves = figure.calculate_possible_moves(self.whites, self.blacks)
                for move in moves:
                    temp_pos = figure.position
                    figure.position = move
                    for a_figure in self.blacks:
                        sim_moves = a_figure.calculate_possible_moves(mines, theirs)
                        for a_move in sim_moves:
                            if a_move[0] == move[0] and a_move[1] == move[1]:
                                moves = list(filter(lambda x: x[0] != move[0] or x[1] != move[1], moves))
                    figure.position = temp_pos
                if len(moves) == 0 and self.check_white:
                    self.winner = FigureColor.BLACK
                break

    def show_moves(self, figure):
        self.init_board()
        self.selected_figure = figure
        mines = self.blacks if self.current_player == FigureColor.BLACK else self.whites
        theirs = self.whites if self.current_player == FigureColor.BLACK else self.blacks
        moves = figure.calculate_possible_moves(mines, theirs)
        king = None

        for b_figure in self.whites if self.current_player == FigureColor.BLACK else self.blacks:
            if isinstance(b_figure, King):
                king = b_figure

        moves = list(filter(lambda x: x[0] != king.position[0] or x[1] != king.position[1], moves))

        if isinstance(figure, King):
            for a_figure in self.whites if self.current_player == FigureColor.BLACK else self.blacks:
                for aMove in moves:
                    tempFigurePos = figure.position
                    figure.position = aMove
                    simMoves = a_figure.calculate_possible_moves(theirs, mines)
                    for move in simMoves:
                        # len(list(filter(lambda x: move[0] == x[0] and move[1] == x[1], moves))) > 0:
                        if aMove[0] == move[0] and aMove[1] == move[1]:
                            moves = list(filter(lambda x: x[0] != move[0] or x[1] != move[1], moves))
                    figure.position = tempFigurePos

        for move in moves:
            for pos in self.positions:
                if move[0] == pos.position[0] and move[1] == pos.position[1]:
                    pos.position_color = PositionColor.SELECTED

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        # self._display_surf.fill((255, 255, 255))
        # Pawn((20,30), FigureColor.WHITE)

        self._running = True
        self.init_board()
        self.init_figures()
        self.current_player = FigureColor.WHITE
        self.selected_figure = None
        self.check_black = False
        self.check_white = False
        self.winner = None
        # self._display_surf.blit(chessImg, (80,80))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONUP:
            if self.winner is not None:
                self.on_init()
                return
            pos = pygame.mouse.get_pos()
            board_pos = []
            board_pos.append(int((pos[0] - ChessConst.START_CORNER[0]) / ChessConst.FIELD_SIZE[0]))
            board_pos.append(int((pos[1] - ChessConst.START_CORNER[1]) / ChessConst.FIELD_SIZE[1]))
            self.resolve_click(board_pos)

        if event.type == 3:
            self.on_init()
            return

    def on_loop(self):
        pass

    def on_render(self):
        font = pygame.font.SysFont("arial", 20)
        self._display_surf.fill((0, 0, 0))
        if self.winner is not None:
            font = pygame.font.SysFont("arial", 60)
            text = font.render("Wygrał " + ("Czarny" if self.winner == FigureColor.BLACK else "Biały"), True,
                               (255, 255, 255))

            self._display_surf.blit(text, (100, 200))
            pygame.display.flip()
            return

        for pos in self.positions:
            pos.draw(self._display_surf)
        for fig in self.whites:
            fig.draw(self._display_surf)
        for fig in self.blacks:
            fig.draw(self._display_surf)

        text = font.render("Ruch: " + ("Czarny " if self.current_player == FigureColor.BLACK else "Biały "), True,
                           (255, 255, 255))
        self._display_surf.blit(text, (100,20))
        text = font.render("Spacja: Reset", True,
                           (255, 255, 255))
        self._display_surf.blit(text, (400, 20))
        if self.check_black:
            text = font.render("Szach Czarny", True, (255, 255, 255))
            self._display_surf.blit(text, (100, 45))
        if self.check_white:
            text = font.render("Szach Biały", True, (255, 255, 255))
            self._display_surf.blit(text, (100, 70))
        pygame.display.flip()
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):

        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()

