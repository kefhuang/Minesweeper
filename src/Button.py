# -*- coding:utf-8 -*-
"""
@author: victorvv
@contact: wengvictor5@gmail.com
@software: PyCharm
@file: Button.py
@time: 2020/7/15 13:11
@description: This file creates button for UI
"""
import pygame

from src.constants import RGB, GAME_LEVEL, INTERMEDIATE_BOARD


class Button:
    def __init__(self, dim, message, bg_colour, message_colour, message_size):
        """
        This function is used to initialise a button with a given message
        The message will be located at the centre of the button
        Args:
            message(String): the message needs to be displayed
            bg_colour(Tuple of 3): the bg color of button
            message_colour(Tuple of 3): the colour of the message
            dim (Tuple of 4): contains where the button is, and the size of the button
        """
        self.bg_colour = bg_colour
        self.message = message
        self.message_colour = message_colour
        self.message_size = message_size
        self.dim = dim

    def draw_button(self, screen):
        """
        This function is used to draw the button on the given screen
        Args:
            screen(String): where the user wants to display the button
        Returns:
            void
        """
        pygame.draw.rect(screen, self.bg_colour, self.dim)
        # Get the font
        font = pygame.font.Font('material/Trinity.ttf', self.message_size)
        text = font.render(self.message, True, self.message_colour)
        tw, th = text.get_size()
        tx = self.dim[0] + self.dim[2] / 2 - tw / 2
        ty = self.dim[1] + self.dim[3] / 2 - th / 2
        screen.blit(text, (tx, ty))

    def is_down(self, pos, screen):
        """
        This function is used to detect if a mousebutton is  down
        And update the display when it is down
        Args:
            pos(Tuple of 2): determines the x, y coordinate of the event
            screen(String): determines the screen to display the updates
        Returns:
            void
        """
        if self.within_bound(pos):
            button = Button(self.dim, self.message, RGB["HAZE"], self.message_colour, self.message_size)
            button.draw_button(screen)
            pygame.display.update()

    def is_up(self, pos, screen):
        """
        This function is used to detect if a mousebutton is up
        And update the display when it is up
        Args:
            pos(Tuple of 2): this determines the x, y coordinates of the event
            screen(String): this determines where the updates would happen

        Returns:
            void
        """
        if self.within_bound(pos):
            self.draw_button(screen)
            pygame.display.update()

    def within_bound(self, pos):
        """
        This function is used to check if an event is happened within boundaries
        Args:
            pos（Tuple of 2): this determines the x, y coordinates of the event
        Returns:
            True if it within the bound
            False, otherwise
        """
        x, y = pos
        if self.dim[0] <= x <= self.dim[0] + self.dim[2] and self.dim[1] <= y <= self.dim[1] + self.dim[3]:
            return True
        return False

    def update_button(self, event, screen):
        """
        This function updates the button when it is clicked
        Args:
            event(Event): This is user's event
            screen(String): This determines the screen to be displayed
        Returns:
            board_size(Dictionary): This determines the dimension of the board
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.is_down(event.pos, screen)
        if event.type == pygame.MOUSEBUTTONUP:
            self.is_up(event.pos, screen)
            return self.get_board_size()

    def get_board_size(self):
        """
        This function is used to ask user to choose the board's size
        # Args:
        #     button_type(String): There are 3 types of board
        #                          Beginner, Intermediate and Customise
        Returns:
            board_size(dictionary): This contains the dimension of the board
        """
        board = {}
        if self.message == GAME_LEVEL["B"]:
            return board
        elif self.message == GAME_LEVEL["I"]:
            board = INTERMEDIATE_BOARD
        else:
            pass
        return board