# -*- coding:utf-8 -*-
"""
@author: victorvv
@contact: wengvictor5@gmail.com
@software: PyCharm
@file: PygameView.py
@time: 2020/7/14 上午10:46
@description: This builds the general GUI for minesweeper
"""
import pygame

from src.view.assets.datas.constants import RGB
from src.view.PygameView.Button import Button
from src.view import View


class PygameView(View):
    """
    This class is used to generate the GUI view
    This class is built by PygameView
    """

    def __init__(self, screen_width=400, screen_height=600):
        """
        Constructor for PygameView
        Args:
            screen_width: default value for screen width is 400
            screen_height: default value for screen height is 600
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Set up the screen
        self.screen = pygame.display.set_mode((screen_width, screen_height), flags=pygame.RESIZABLE)
        self.screen.fill(RGB["WHITE"])
        pygame.display.set_caption("Minesweeper")
        # Generate the event
        self.event = pygame.event.wait()

    def get_board_size(self):
        """
        This function is used initialise the game
        And get the board size of the game
        Returns:
            game_level(dictionary): This determines the dimension of the board
        """
        # Dimension of button
        ratio = self.screen_height // self.screen_width
        BUTTON_WIDTH = ratio * 200
        BUTTON_HEIGHT = ratio * 50
        MESSAGE_SIZE = ratio * 20
        all_button_height = BUTTON_HEIGHT * 3 + 200

        # Set up the option buttons
        # Set up beginner button
        beginner_button = Button(
            (self.screen_width // 2 - BUTTON_WIDTH // 2, (self.screen_height - all_button_height) // 2, BUTTON_WIDTH,
             BUTTON_HEIGHT),
            RGB["PALE_GREEN"], "Beginner", RGB["WHITE"], MESSAGE_SIZE)
        beginner_button.draw_button(self.screen)

        # Set up intermediate button
        intermediate_button = Button(
            (self.screen_width // 2 - BUTTON_WIDTH // 2, (self.screen_height - all_button_height) // 2 + (100 * ratio),
             BUTTON_WIDTH, BUTTON_HEIGHT),
            RGB["PALE_GREEN"], "Intermediate", RGB["WHITE"], MESSAGE_SIZE)
        intermediate_button.draw_button(self.screen)

        # Set up customise button
        customise_button = Button(
            (self.screen_width // 2 - BUTTON_WIDTH // 2, (self.screen_height - all_button_height) // 2 + (200 * ratio),
             BUTTON_WIDTH, BUTTON_HEIGHT),
            RGB["PALE_GREEN"], "Customise", RGB["WHITE"], MESSAGE_SIZE)
        customise_button.draw_button(self.screen)

        # First time set up the screen
        pygame.display.flip()

        # Get the game level
        while True:
            if beginner_button.update_button(self.event, self.screen):
                pygame.display.update()
                return beginner_button.update_button(self.event, self.screen)

            elif intermediate_button.update_button(self.event, self.screen):
                pygame.display.update()
                return intermediate_button.update_button(self.event, self.screen)

            else:
                pygame.display.update()
                return customise_button.update_button(self.event, self.screen)

    def draw(self, board):
        """
        This function is used to draw the board, and update the board
        Args:
            board: the selected board
        Returns:
            void
        """
        # Dimension of cell
        ratio = self.screen_height // self.screen_width
        CELL_WIDTH = ratio * 20
        CELL_HEIGHT = ratio * 20
        NUMBER_SIZE = CELL_HEIGHT // CELL_WIDTH * 10 * ratio

        # Get the dimension of the board
        rows = len(board)
        cols = len(board[0])
        for y in range(rows):
            # Draw the y axis
            pygame.draw.line(self.screen, RGB["CYANINE"], (0, CELL_HEIGHT * y), (self.screen_width, CELL_HEIGHT * y), 5)
            for x in range(cols):
                # Draw the x axis
                pygame.draw.line(self.screen, RGB["CYANINE"], (CELL_WIDTH * x, 0), (CELL_WIDTH * x, self.screen_height), 5)
                point = board[y][x]
                if point.is_opened:
                    # Load the image of mine to the screen
                    if point.is_bomb:
                        bomb = pygame.image.load('src/View/assets/images/mine.jpg')
                        bomb = pygame.transform.smoothscale(bomb, (CELL_WIDTH, CELL_HEIGHT))
                        self.screen.blit(bomb, (x * CELL_WIDTH + 5, y * CELL_HEIGHT + 5))
                        continue
                    # Draw the point out
                    bx = x * CELL_WIDTH - 5
                    by = y * CELL_HEIGHT - 5
                    bw = CELL_WIDTH - 5
                    bh = CELL_HEIGHT - 5
                    pygame.draw.rect(self.screen, RGB["HAZE"], (bx, by, bw, bh), 5)
                    number_font = pygame.font.Font('src/View/assets/fonts/number.ttf', NUMBER_SIZE)
                    number = number_font.render(point, True, RGB[str(point)])
                    tw, th = number.get_size()
                    # Centralise the number
                    tx = bx + bw / 2 - tw / 2
                    ty = by + bh / 2 - th / 2
                    self.screen.blit(number, (tx, ty))

                if point.is_flagged:
                    # Load the image of flag to the screen
                    flag = pygame.image.load('src/View/assets/images/flag.png')
                    flag = pygame.transform.smoothscale(flag, (CELL_WIDTH, CELL_HEIGHT))
                    self.screen.blit(flag, (x * CELL_WIDTH + 5, y * CELL_HEIGHT + 5))
                    continue

                # Draw squares for unopened point on the board
                bx = x * CELL_WIDTH - 5
                by = y * CELL_HEIGHT - 5
                bw = CELL_WIDTH - 5
                bh = CELL_HEIGHT - 5
                pygame.draw.rect(self.screen, RGB["PALE_GREEN"], (bx, by, bw, bh))

        # Update the screen after changing
        pygame.display.update()


    def fail(self):
        """
        Deal with the situation when game fails
        Returns:
            continune(boolean): True is start. False otherwise
        """
        # Dimension of the button
        ratio = self.screen_height // self.screen_width
        DEMAND_SIZE = ratio * 30
        MESSAGE_SIZE = ratio * 20

        self.screen.fill(RGB["WHITE"])
        bx, by, bw, bh = (self.screen_width / 4, self.screen_height / 4, self.screen_width / 2, self.screen_height / 6)
        pygame.draw.rect(self.screen, RGB["PALE_GREEN"], (bx, by, bw, bh))
        # Get the font
        font = pygame.font.Font('src/View/assets/fonts/Trinity.ttf', DEMAND_SIZE)
        text = font.render("You've met a bomb", True, RGB["WHITE"])
        tw, th = text.get_size()
        # Centralise the text
        tx = bx + bw / 2 - tw / 2
        ty = by + bh / 2 - th / 2
        self.screen.blit(text, (tx, ty))

        # Create two buttons
        restart_button = Button((self.screen_width / 4, self.screen_height / 2, self.screen_width / 3, self.screen_height / 10), RGB["PALE_GREEN"],
                                "RESTART", RGB["WHITE"], MESSAGE_SIZE)
        quit_button = Button((self.screen_width * 2 / 3, self.screen_heights / 2, self.screen_width / 3, self.screen_height / 10), RGB["PALE_GREEN"],
                            "QUIT", RGB["WHITE"], MESSAGE_SIZE)
        # Get user's choice
        while True:
            if restart_button.is_up(self.event.pos, self.screen):
                pygame.display.update()
                return restart_button.get_choice(self.event, self.screen)
            if quit_button.is_up(self.event.pos, self.screen):
                pygame.display.update()
                return quit_button.get_choice(self.event, self.screen)

    def win(self):
        """
        Deal with the situation when game wins
        Returns:
            continune(boolean): True is start. False otherwise
        """
        # Dimension of the button
        ratio = self.screen_height // self.screen_width
        DEMAND_SIZE = ratio * 30
        MESSAGE_SIZE = ratio * 20

        self.screen.fill(RGB["WHITE"])
        bx, by, bw, bh = (self.screen_width / 4, self.screen_height / 4, self.screen_width / 2, self.screen_height / 6)
        pygame.draw.rect(self.screen, RGB["PALE_GREEN"], (bx, by, bw, bh))

        # Get the font
        font = pygame.font.Font('src/View/assets/fonts/Trinity.ttf', DEMAND_SIZE)
        text = font.render("Wow! Excellent", True, RGB["WHITE"])
        tw, th = text.get_size()
        # Centralise the text
        tx = bx + bw / 2 - tw / 2
        ty = by + bh / 2 - th / 2
        self.screen.blit(text, (tx, ty))

        # Create two buttons
        restart_button = Button((self.screen_width / 4, self.screen_height / 2, self.screen_width / 3, self.screen_height / 10), RGB["PALE_GREEN"],
                                "RESTART", RGB["WHITE"], MESSAGE_SIZE)
        quit_button = Button((self.screen_width * 2 / 3, self.screen_height / 2, self.screen_width / 3, self.screen_height / 10), RGB["PALE_GREEN"],
                            "QUIT", RGB["WHITE"], MESSAGE_SIZE)
        # Get user's choice
        while True:
            if restart_button.is_up(self.event.pos, self.screen):
                pygame.display.update()
                return restart_button.get_choice(self.event, self.screen)
            if quit_button.is_up(self.event.pos, self.screen):
                pygame.display.update()
                return quit_button.get_choice(self.event, self.screen)


    def _get_board_coordinates(self, pos, board):
        """
        This function is used to return the x, y coordinate of the updated point on the board
        Args:
            pos(int, int): event's pos
            board(matrix of PointData): the output board
        Returns:
            coordinates(int, int): the x, y value of the point on the board
        """
        # Dimension of cell
        ratio = self.screen_height // self.screen_width
        CELL_WIDTH = ratio * 20
        CELL_HEIGHT = ratio * 20

        x, y = pos
        rows = len(board)
        cols = len(board[0])
        for r in range(rows):
            for c in range(cols):
                bx = c * CELL_WIDTH - 5
                by = r * CELL_HEIGHT - 5
                bw = CELL_WIDTH - 5
                bh = CELL_HEIGHT - 5
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    return c, r

    def input(self, board):
        """
        This function return user's move
        Returns:
            user_move{"POS": (int, int), "OPEN": boolean, "FLAG": bool}
        """
        user_move = {}

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                user_move["flag"] = False
                user_move["x"] = self._get_board_coordinates(event.pos, board)[0]
                user_move["y"] = self._get_board_coordinates(event.pos, board)[1]
                return user_move
            elif event.type == pygame and event.button == 3:
                user_move["flag"] = True
                user_move["x"] = self._get_board_coordinates(event.pos, board)[0]
                user_move["y"] = self._get_board_coordinates(event.pos, board)[1]
                return user_move

# To be added
#
# while True:
#
#         # elif event.type == material.VIDEORESIZE:
#         #     size = width, height = event.size[0], event.size[1]
#         #     screen = material.display.set_mode(size, material.RESIZABLE)
#         #     screen.blit(material.transform.scale(img, size), (0, 0))
#         #     material.display.flip()
#
#         board_size = beginner_button.update_button(event, window)
#         # print(board_size)
#         intermediate_button.update_button(event, window)
#         customise_button.update_button(event, window)


# # The section below is for test purposes
#
# def test():
#     from src.Board import Board
#
#
#
# if __name__ == '__main__':
#     test()
